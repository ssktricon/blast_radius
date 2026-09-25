You are analyzing a unified diff for a contract change.

Goal:
- identify changed members
- classify the change as breaking, additive, or internal
- return evidence from the diff

Rules:
- property rename is breaking
- property addition is additive
- no semantic mutation is internal
- do not speculate beyond the diff
