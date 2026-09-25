from src.orchestrator.orchestrator import run_contract_analysis


def test_orchestrator_calls_contract_stream():
    with open("fixtures/producer_consumer_breaking.diff", "r", encoding="utf-8") as handle:
        payload = run_contract_analysis(diff_text=handle.read())

    assert len(payload) == 1
    assert payload[0]["classification"] == "breaking"
