from src.analyzers.contract_analysis import analyze_contract_diff


SAMPLE_DIFF = '''diff --git a/OrderCreated.cs b/OrderCreated.cs
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


def test_breaking_property_rename_is_detected():
    changes = analyze_contract_diff(SAMPLE_DIFF)

    assert len(changes) == 1
    assert changes[0]["member"] == "Amount"
    assert changes[0]["before"] == "Amount"
    assert changes[0]["after"] == "TotalAmount"
    assert changes[0]["classification"] == "breaking"
    assert "contract" in changes[0]["evidence"].lower()


def test_additive_property_is_not_breaking():
    diff = '''diff --git a/OrderCreated.cs b/OrderCreated.cs
index 1111111..2222222 100644
--- a/OrderCreated.cs
+++ b/OrderCreated.cs
@@
 public record OrderCreated
 {
     public Guid OrderId { get; init; }
+    public string? Currency { get; init; }
 }
'''

    changes = analyze_contract_diff(diff)

    assert len(changes) == 1
    assert changes[0]["classification"] == "additive"


def test_rule_based_classification_uses_yaml_config():
    diff = '''diff --git a/OrderCreated.cs b/OrderCreated.cs
index 1111111..2222222 100644
--- a/OrderCreated.cs
+++ b/OrderCreated.cs
@@
 public record OrderCreated
 {
-    public decimal Amount { get; init; }
+    public decimal TotalAmount { get; init; }
 }
'''

    changes = analyze_contract_diff(diff, config_path="config/rules.yaml")
    assert changes[0]["classification"] == "breaking"
    assert changes[0]["evidence"]


def test_realistic_producer_consumer_fixture_is_detected():
    with open("fixtures/producer_consumer_breaking.diff", "r", encoding="utf-8") as handle:
        diff = handle.read()

    changes = analyze_contract_diff(diff, config_path="config/rules.yaml")
    assert any(change["member"] == "Amount" for change in changes)
    assert any(change["classification"] == "breaking" for change in changes)
