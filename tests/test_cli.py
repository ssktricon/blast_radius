import json

from src.orchestrator.orchestrator import run_contract_analysis


def test_cli_outputs_structured_contract_result(capsys):
    diff = '''diff --git a/OrderCreated.cs b/OrderCreated.cs
index 1111111..2222222 100644
--- a/OrderCreated.cs
+++ b/OrderCreated.cs
@@
 public record OrderCreated
 {
-    public decimal Amount { get; init; }
+    public decimal TotalAmount { get; init; }
     public Guid OrderId { get; init; }
 }
'''

    payload = run_contract_analysis(diff_text=diff)
    captured = capsys.readouterr()

    assert payload[0]['classification'] == 'breaking'
    assert payload[0]['member'] == 'Amount'
    assert payload[0]['before'] == 'Amount'
    assert payload[0]['after'] == 'TotalAmount'
    assert captured.out == ''
