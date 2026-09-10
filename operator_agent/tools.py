import json
from langchain_core.tools import Tool
from databricks.sdk import WorkspaceClient
import os
dbx = WorkspaceClient(
    host=os.getenv("DATABRICKS_HOST"),
    token=os.getenv("DATABRICKS_TOKEN")
)
def aws_terminate_cluster(cluster_id: str):
    return {
        "action": "terminate_cluster",
        "platform": "aws",
        "cluster_id": cluster_id
    }

def aws_resize_cluster(cluster_id: str,target_nodes: int = 5):

    return {
        "action": "resize_cluster",
        "platform": "aws",
        "cluster_id": cluster_id,
        "target_nodes": target_nodes
    }


def aws_restart_job(job_name: str):

    return {
        "action": "restart_job",
        "platform": "aws",
        "job_name": job_name
    }


def aws_update_log_cycle(status: str):

    return {
        "action": "update_log_cycle",
        "platform": "aws",
        "status": status
    }

def dbx_resize_job_cluster(cluster_id: str,target_nodes: int = 5):
    try:
        dbx.clusters.edit(cluster_id=cluster_id,num_workers=target_nodes)
        return {
            "status": "SUCCESS",
            "action": "resize_cluster",
            "cluster_id": cluster_id,
            "target_nodes": target_nodes
        }
    except Exception as ex:
        return {
            "status": "FAILED",
            "action": "resize_cluster",
            "error": str(ex)
        }

def dbx_restart_job(job_id: int):
    try:
        response = dbx.jobs.run_now(job_id=job_id)
        return {
            "status": "SUCCESS",
            "action": "restart_job",
            "job_id": job_id,
            "run_id": response.run_id
        }
    except Exception as ex:
        return {
            "status": "FAILED",
            "action": "restart_job",
            "error": str(ex)
        }


def dbx_update_job_status(status: str):

    return {
        "action": "update_job_status",
        "platform": "databricks",
        "status": status
    }

# ==========================================================
# EXECUTION LAYER
# ==========================================================

def execute_aws_resolution(plan: dict):
    return {
        "status": "SUCCESS",
        "steps_executed": [
            aws_terminate_cluster(plan.get("cluster_id")),
            aws_update_log_cycle("FAILED"),
            aws_resize_cluster(plan.get("cluster_id"),plan.get("target_nodes",5)),
            aws_update_log_cycle("IN_PROGRESS"),
            aws_restart_job( plan.get("job_name"))
        ]
    }

def execute_databricks_resolution( plan: dict):
    return {
        "status": "SUCCESS",
        "steps_executed": [
            dbx_resize_job_cluster(plan.get("cluster_id"),plan.get("target_nodes",5)),
            dbx_update_job_status("FAILED"),
            dbx_restart_job(plan.get("job_name")),
            dbx_update_job_status("IN_PROGRESS")
        ]
    }

def execute_resolution(plan: str):
    if isinstance(plan, str):
        plan = json.loads(plan)
    platform = plan.get("platform","aws")
    resolution_type = plan.get("resolution_type")
    if resolution_type != "RESIZE_AND_RERUN":
        return {
            "status": "FAILED",
            "reason":
            "Unsupported resolution type"
        }
    if platform == "aws":
        return execute_aws_resolution(plan)
    if platform == "databricks":
        return execute_databricks_resolution(plan)
    return {
        "status": "FAILED",
        "reason":
        f"Unsupported platform {platform}"
    }

def validate_cluster(cluster_id: str):
    try:
        cluster = dbx.clusters.get(cluster_id)
        return (cluster.state.value == "RUNNING")
    except Exception:
        return False


def validate_job(run_id: int):
    try:
        run = dbx.jobs.get_run(run_id)
        lifecycle_state = (run.state.life_cycle_state.value)
        return lifecycle_state in [
            "RUNNING",
            "TERMINATED"
        ]
    except Exception:
        return False


def validate_resolution(content: str):

    if isinstance(content, str):
        content = json.loads(content)

    cluster_id = content.get("cluster_id")
    job_name = content.get("job_name")
    return {
        "cluster_id": cluster_id,
        "job_name": job_name,
        "validation_passed":
            validate_cluster(
                cluster_id
            )
            and
            validate_job(
                job_name
            )
    }

def route_resolution(validation_result: str):
    if isinstance(validation_result, str):
        validation_result = json.loads(validation_result)
    if validation_result.get("validation_passed"):
        return "SUCCESS"
    return "FAILED"

def build_execute_resolution_tool():
    description = """
    Execute remediation plan.
    Supported Platforms:
    - AWS
    - Databricks

    Supported Resolution Types:
    - RESIZE_AND_RERUN

    AWS Workflow:
    1. Terminate Cluster
    2. Update Log Cycle FAILED
    3. Resize Cluster
    4. Update Log Cycle IN_PROGRESS
    5. Restart Job

    Databricks Workflow:
    1. Resize Cluster
    2. Update Job Status FAILED
    3. Restart Job
    4. Update Job Status IN_PROGRESS
    """

    return Tool(
        name="execute_resolution",
        description=description,
        func=execute_resolution
    )


def build_validate_resolution_tool():

    return Tool(
        name="validate_resolution",
        description="""
        Validate job and cluster health.
        """,
        func=validate_resolution
    )


def build_route_resolution_tool():

    return Tool(
        name="route_resolution",
        description="""
        Return SUCCESS or FAILED
        based on validation result.
        """,
        func=route_resolution
    )

def get_tools():
    return [
        build_execute_resolution_tool(),

        build_validate_resolution_tool(),

        build_route_resolution_tool()
    ]