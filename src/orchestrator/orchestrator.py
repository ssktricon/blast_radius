from __future__ import annotations

import json
from pathlib import Path

from src.analyzers.contract_analysis import analyze_contract_diff


def run_contract_analysis(diff_text: str | None = None, diff_file: str | None = None) -> list[dict]:
    """Thin orchestration layer that calls the contract-analysis stream.

    This remains independent of downstream streams and is designed to be plugged into a larger orchestrator later.
    """
    if diff_text is None and diff_file is not None:
        path = Path(diff_file)
        diff_text = path.read_text(encoding="utf-8") if path.exists() else ""

    if diff_text is None:
        return []

    return analyze_contract_diff(diff_text, config_path="config/rules.yaml")


def main() -> int:
    diff_path = Path("fixtures/producer_consumer_breaking.diff")
    result = run_contract_analysis(diff_file=str(diff_path))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
