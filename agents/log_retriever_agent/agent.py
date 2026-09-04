"""Log Retriever Agent - fetches CloudWatch/S3 logs for the failing workload."""

from agents.common.agent.base_agent import AgentBase
from agents.log_retriever_agent.tools import get_cloudwatch_logs, get_s3_logs


class LogRetrieverAgent(AgentBase):

    @property
    def name(self) -> str:
        return "log_retriever_agent"

    @property
    def description(self) -> str:
        return "Retrieves error logs from CloudWatch and S3 for classification."

    def invoke(self, state: dict) -> dict:
        state["cloudwatch_logs"] = get_cloudwatch_logs(
            log_group=state.get("log_group", ""),
            start_time=state.get("start_time", 0),
            end_time=state.get("end_time", 0),
        )
        state["s3_logs"] = get_s3_logs(
            bucket=state.get("log_bucket", ""),
            prefix=state.get("log_prefix", ""),
        )
        state["next_agent"] = "error_classifier_agent"
        return state
