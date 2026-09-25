# Blast Radius - Contract & Change Analysis

This repository contains the local-first implementation for the `Contract & Change Analysis` stream of the Blast Radius MVP.

## Purpose

This module is intentionally independent from the other workstreams:

- no GitHub API dependency
- no LLM dependency
- no NetworkX graph dependency
- no downstream consumer analysis
- no test execution logic

Its sole purpose is to analyze a unified diff and classify contract changes deterministically.

## Project structure

```text
blast-radius/
├── action.yml
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   ├── orchestrator/
│   ├── analyzers/
│   ├── graph/
│   ├── ai/
│   ├── tests/
│   ├── report/
│   └── ci/
├── config/
│   ├── services.yaml
│   └── rules.yaml
├── prompts/
│   ├── contract_analysis.md
│   ├── consumer_impact.md
│   ├── test_analysis.md
│   ├── failure_analysis.md
│   └── report_generation.md
├── graph/
│   └── graph.json
├── fixtures/
│   ├── producer_consumer_breaking.diff
│   └── producer_consumer_additive.diff
├── demo.diff
├── .github/
│   └── workflows/
└── .venv/
```

## What it detects

The analyzer can detect:

- breaking changes where a contract member is renamed
- additive changes where a new property is added
- internal/no-op changes where there is no real contract mutation

## Demo scenario mapping

This stream matches the project-level design in the Blast Radius plan:

- `blast-radius-demo-api` is the producer repository.
- `blast-radius-demo-consumer-1` is a downstream consumer that reads the changed contract field.
- `blast-radius-demo-consumer-2` is a second downstream consumer that may or may not read the changed field.

The fixture files under `fixtures/` model the same idea locally:

- `producer_consumer_breaking.diff` simulates the `Amount -> TotalAmount` contract rename.
- `producer_consumer_additive.diff` simulates a safe additive field addition.

The config file at `config/services.yaml` describes the same dependency relationship in a minimal YAML form.

## Local execution

From the repo root:

```powershell
python -m src.orchestrator.orchestrator
```

## Example output

```json
[
  {
    "contract": "OrderCreated.cs",
    "member": "Amount",
    "before": "Amount",
    "after": "TotalAmount",
    "classification": "breaking",
    "evidence": "Contract change detected in OrderCreated.cs: member 'Amount' renamed to 'TotalAmount' in the diff."
  }
]
```

## Classification rules

The current deterministic rules are:

- rename of an existing public property => `breaking`
- new property added => `additive`
- no semantic change detected => `internal`

## Validation

Run tests with:

```powershell
cd "C:\Users\Seliz.Koshy\Documents\GitHub\blast_radius"
.\.venv\Scripts\python -m pytest -q
```

Current result: 3 pass

## Boundary

This stream owns only:

- diff parsing
- contract member comparison
- classification
- structured JSON output

It does not own:

- GitHub orchestration
- dependency graph generation
- LLM reasoning
- test selection
- report presentation
