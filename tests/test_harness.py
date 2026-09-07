import os
import tempfile
from harness.agent_harness import AgentHarness

def test_harness_execution_and_assertion():
    harness = AgentHarness()
    result = harness.run("Sustentabilidade e Economia Circular")

    assert result["status"] == "COMPLETED"
    assert harness.assert_state_transition(["ResearcherAgent", "WriterAgent", "EvaluatorNode"])

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        audit_file = harness.export_audit_log(tmp_path)
        assert os.path.exists(audit_file)
        assert os.path.getsize(audit_file) > 0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
