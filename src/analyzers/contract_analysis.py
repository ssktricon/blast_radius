from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


PROPERTY_PATTERN = re.compile(
    r"^(?P<op>[+-])\s*(?:public|private|internal|protected)?\s*(?:static\s+)?"
    r"(?:[\w<>\[\],\.\?]+)\s+(?P<name>\w+)\s*\{\s*get;\s*init;\s*\}",
    re.MULTILINE,
)


def _load_rules(config_path: str | None) -> dict:
    if not config_path or yaml is None:
        return {}

    path = Path(config_path)
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def _extract_contract_name(diff_text: str) -> str:
    match = re.search(r"diff --git a/(.+?) b/", diff_text)
    return match.group(1) if match else "unknown-contract"


def _extract_property_changes(diff_text: str) -> tuple[str | None, str | None, list[str]]:
    removed = []
    added = []

    for line in diff_text.splitlines():
        match = PROPERTY_PATTERN.match(line)
        if not match:
            continue

        name = match.group("name")
        if match.group("op") == "-":
            removed.append(name)
        else:
            added.append(name)

    return (removed[0] if removed else None, added[0] if added else None, added)


def _classify_change(before_member: str | None, after_member: str | None, added_members: list[str]) -> str:
    if before_member and after_member and before_member != after_member:
        return "breaking"
    if before_member and after_member and before_member == after_member:
        return "internal"
    if added_members:
        return "additive"
    return "internal"


def analyze_contract_diff(diff_text: str, config_path: str | None = None) -> list[dict]:
    """Analyze a diff and return structured contract changes.

    This function is intentionally independent of GitHub, AI, dependency graph, and test execution logic.
    """
    if not diff_text or "@@" not in diff_text:
        return []

    _ = _load_rules(config_path)
    contract_name = _extract_contract_name(diff_text)
    before_member, after_member, added_members = _extract_property_changes(diff_text)
    classification = _classify_change(before_member, after_member, added_members)

    if before_member and after_member and before_member != after_member:
        return [{
            "contract": contract_name,
            "member": before_member,
            "before": before_member,
            "after": after_member,
            "classification": classification,
            "evidence": f"Contract change detected in {contract_name}: member '{before_member}' renamed to '{after_member}' in the diff."
        }]

    if added_members:
        new_member = added_members[0]
        return [{
            "contract": contract_name,
            "member": new_member,
            "before": None,
            "after": new_member,
            "classification": classification,
            "evidence": f"Additive contract change detected in {contract_name}: new member '{new_member}' was added."
        }]

    return [{
        "contract": contract_name,
        "member": "unknown",
        "before": None,
        "after": None,
        "classification": "internal",
        "evidence": f"No contract member mutation detected in {contract_name}."
    }]
