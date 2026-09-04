from agents.supervisor_agent.agent import SupervisorAgent


def test_supervisor_routes_new_incident_to_log_retriever(mocker):
    mocker.patch("agents.supervisor_agent.agent.find_known_incident", return_value=None)

    state = SupervisorAgent().invoke({"error_type": "OOM", "error_message": "executor lost"})

    assert state["incident_exists"] is False
    assert state["next_agent"] == "log_retriever_agent"
