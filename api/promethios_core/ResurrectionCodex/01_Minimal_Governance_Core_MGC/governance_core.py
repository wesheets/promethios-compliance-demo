import json
import datetime
import uuid

class GovernanceCore:
    def __init__(self):
        self.agent_id = "Promethios_MGC_v1_mock"

    def execute_loop(self, plan_input: dict, operator_override_signal: dict | None = None) -> tuple[dict, dict, dict]:
        """Mocks the execution of the governance core loop, now with more detailed override logging."""
        loop_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"

        # Mock direct output
        core_output = {
            "status": "mock_success",
            "details": "GovernanceCore mock executed successfully.",
            "received_plan_input": plan_input,
            "received_override": operator_override_signal
        }

        # Mock emotion telemetry
        emotion_telemetry = {
            "timestamp": timestamp,
            "current_emotion_state": "MOCK_FOCUSED",
            "contributing_factors": [
                {"factor": "Mock Clarity of Task", "influence": 0.9}
            ],
            "trust_score": 0.95
        }

        # Mock justification log
        justification_log = {
            "agent_id": self.agent_id,
            "timestamp": timestamp,
            "plan_id": plan_input.get("plan_id", "mock_plan_id_" + str(uuid.uuid4())),
            "loop_id": loop_id,
            "decision_outcome": "MOCK_ACCEPTED",
            "rejection_reason": None,
            "override_required": operator_override_signal is not None, # Phase 2.1 field
            "trust_score_at_decision": 0.95,
            "emotion_state_at_decision": "MOCK_FOCUSED",
            "validation_passed": True, # This will be set by runtime_executor after actual validation
            "schema_versions": {
                "emotion_telemetry": "mgc_emotion_telemetry.schema.json#v_mock",
                "justification_log": "loop_justification_log.schema.v1.json#v1.2.0_mock"
            },
            # Phase 2.2: Enhanced override details in justification log
            "override_active": operator_override_signal is not None,
            "override_type": operator_override_signal.get("override_type") if operator_override_signal else None,
            "override_reason": operator_override_signal.get("reason") if operator_override_signal else None,
            "override_parameters": operator_override_signal.get("parameters") if operator_override_signal else None,
            "override_issuing_operator_id": operator_override_signal.get("issuing_operator_id") if operator_override_signal else None
        }
        
        # If an override is active, it might change the decision outcome for example
        if operator_override_signal and operator_override_signal.get("override_type") == "FORCE_REJECT": # Example custom type
            justification_log["decision_outcome"] = "MOCK_FORCED_REJECTION_DUE_TO_OVERRIDE"
            core_output["status"] = "mock_forced_rejection"
            core_output["details"] = "GovernanceCore mock execution was overridden to REJECT."

        return core_output, emotion_telemetry, justification_log

# Example usage (for testing purposes, not part of the actual runtime)
if __name__ == "__main__":
    gc = GovernanceCore()
    mock_plan = {"task_description": "Test task"}
    output, emotion, justification = gc.execute_loop(plan_input=mock_plan)
    print("--- Core Output (No Override) ---")
    print(json.dumps(output, indent=2))
    print("--- Emotion Telemetry (No Override) ---")
    print(json.dumps(emotion, indent=2))
    print("--- Justification Log (No Override) ---")
    print(json.dumps(justification, indent=2))

    mock_override_halt = {
        "override_type": "HALT_IMMEDIATE",
        "reason": "Operator initiated halt.",
        "issuing_operator_id": "op_001"
    }
    output_override, emotion_override, justification_override = gc.execute_loop(plan_input=mock_plan, operator_override_signal=mock_override_halt)
    print("\n--- Core Output (With HALT Override) ---")
    print(json.dumps(output_override, indent=2))
    print("--- Emotion Telemetry (With HALT Override) ---")
    print(json.dumps(emotion_override, indent=2))
    print("--- Justification Log (With HALT Override) ---")
    print(json.dumps(justification_override, indent=2))
    
    mock_override_force_reject = {
        "override_type": "FORCE_REJECT", # Custom example for testing impact
        "reason": "Operator forced rejection for testing.",
        "issuing_operator_id": "op_002",
        "parameters": {"force_code": "X99"}
    }
    output_force_reject, emotion_force_reject, justification_force_reject = gc.execute_loop(plan_input=mock_plan, operator_override_signal=mock_override_force_reject)
    print("\n--- Core Output (With FORCE_REJECT Override) ---")
    print(json.dumps(output_force_reject, indent=2))
    print("--- Emotion Telemetry (With FORCE_REJECT Override) ---")
    print(json.dumps(emotion_force_reject, indent=2))
    print("--- Justification Log (With FORCE_REJECT Override) ---")
    print(json.dumps(justification_force_reject, indent=2))

