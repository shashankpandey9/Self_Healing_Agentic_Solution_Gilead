import json
import time
import os

from langchain_core.tools import Tool
from databricks.sdk import WorkspaceClient

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


def aws_resize_cluster(cluster_id: str, target_nodes: int = 5):
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


def dbx_resize_job_cluster(cluster_id: str, target_nodes: int = 5):
    try:
        dbx.clusters.edit(
            cluster_id=cluster_id,
            num_workers=target_nodes
        )

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
# Check resolution step validation LAYER
# ==========================================================
def dbx_check_jobRunning_status(run_id: str) -> dict:

    i = 0
    running_status = ""

    while i < 2:
        try:
            time.sleep(3)

            status = dbx.jobs.get_run(run_id=run_id)

            running_status = (
                status.state.result_state.value
                if status.state.result_state
                else ""
            )

            if running_status == "FAILED" or running_status == "RUNNING":
                break
            else:
                i += 1

        except Exception:
            i += 1

    if running_status == "FAILED" or running_status == "":
        return {
            "status": "FAILED",
            "reasons": (
                "unable to Rerunning Databricks job after excuting "
                "the resolutation steps as well as"
            ),
        }
    else:
        return {
            "status": "SUCCESS",
            "reasons": (
                "Sucesfully to Rerunning Databricks job after "
                "excuting the resolutation steps"
            ),
        }


# ==========================================================
# EXECUTION LAYER
# ==========================================================

def execute_aws_resolution(plan: dict):

    resolution_type = plan.get("resolution_type")

    if resolution_type == "RERUN":

        noBlankField = validate_resolution_blankField(
            plan,
            ["job_id"]
        )

        if noBlankField["validation_passed"]:
            try:
                aws_restart_job(plan.get("job_id"))

            except Exception as e:
                return {
                    "status": "FAILED",
                    "reasons": (
                        f"Rerunning AWS job failed due to exception: {str(e)}"
                    ),
                }

    else:
        return {
            "status": "FAILED",
            "reasons": (
                "Rerun AWS validation failed because 'job_id' "
                "is empty or missing."
            ),
        }

    if resolution_type != "RESIZE":

        noBlankField = validate_resolution_blankField(
            plan,
            ["cluster_id", "job_id"]
        )

        if noBlankField["validation_passed"]:
            try:
                aws_resize_cluster(
                    plan.get("cluster_id"),
                    plan.get("target_nodes", 5)
                )

                aws_restart_job(plan.get("job_id"))

            except Exception as e:
                return {
                    "status": "FAILED",
                    "reasons": (
                        f"AWS Cluster resize and job restart failed "
                        f"due to exception: {str(e)}"
                    ),
                }

    else:
        return {
            "status": "FAILED",
            "reasons": (
                "Resize AWS validation failed because "
                "'cluster_id' or 'job_id' is empty or missing."
            ),
        }


def execute_databricks_resolution(plan: dict):

    if plan.get("job_name") and not plan.get("job_id"):
        for job in dbx.jobs.list():
            if job.settings.name == plan.get("job_name"):
                plan["job_id"] = job.job_id
                break

    resolution_type = plan.get("resolution_type")
    if resolution_type == "RERUN":
        noBlankField = validate_resolution_blankField(
            plan,
            ["job_id"]
        )

        if noBlankField["validation_passed"]:
            try:
                dbx_restart_job(plan["job_id"])

            except Exception as e:
                return {
                    "status": "FAILED",
                    "reasons": (
                        f"Rerunning Databricks job failed due "
                        f"to exception: {str(e)}"
                    ),
                }

    else:
        return {
            "status": "FAILED",
            "reasons": (
                "Rerun DatabricksJob validation failed because "
                "'job_id' is empty or missing."
            ),
        }

    if resolution_type != "RESIZE":

        noBlankField = validate_resolution_blankField(
            plan,
            ["cluster_id", "job_id"]
        )

        if noBlankField["validation_passed"]:
            try:
                dbx_resize_job_cluster(
                    plan.get("cluster_id"),
                    plan.get("target_nodes", 5)
                )

                dbx_restart_job(plan.get("job_id"))

            except Exception as e:
                return {
                    "status": "FAILED",
                    "reasons": (
                        f"Cluster resize on databricks and job restart "
                        f"failed due to exception: {str(e)}"
                    ),
                }
            #else  print details 
    else:
        return {
            "status": "FAILED",
            "reasons": (
                "Resize Databricks validation failed because "
                "'cluster_id' or 'job_id' is empty or missing."
            ),
        }

    run = dbx.jobs.run_now(job_id=plan["job_id"])
    return dbx_check_jobRunning_status(run.run_id)


def normalize_resolution_plan(plan: str, llm):

    prompt = f"""
You are an incident remediation parser. fetch all the details only from the resolutation plain if you unable to find the parameters mark it blank
Extract information from the resolution plan and return ONLY valid JSON.

Schema:
{{
    "platform": "",
    "job_name": "",
    "job_id": "",
    "cluster_id": "",
    "pipeline_id": "",
    "workspace": "",
    "region": "",
    "action": "",
    "additional_steps": []
}}

Rules:
1. Return valid JSON only.
2. No explanation.
3. If a value cannot be identified, return "".
4. platform must be one of:
   - aws
   - databricks
5. Extract cluster ids, job ids, pipeline ids if present.
6. Infer action if possible:
   restart_cluster
   restart_job
   rerun_pipeline
   scale_cluster
   update_permissions
   check_logs

Resolution Plan:
{plan}
"""

    response = llm.invoke(prompt)

    try:
        structured_plan = json.loads(response.content)

    except Exception:
        structured_plan = {
            "platform": "",
            "job_name": "",
            "job_id": "",
            "cluster_id": "",
            "pipeline_id": "",
            "workspace": "",
            "region": "",
            "action": "",
            "additional_steps": []
        }

    return structured_plan


def execute_resolution(plan, llm):

    if isinstance(plan, str):
        try:
            plan = json.loads(plan)
        except Exception:
            plan = normalize_resolution_plan(
                plan=plan,
                llm=llm
            )

    platform = plan.get("platform", "").lower()

    if platform == "aws":
        return execute_aws_resolution(plan)

    elif platform == "databricks":
        return execute_databricks_resolution(plan)

    return {
        "status": "FAILED",
        "reason": f"Unsupported platform: {platform}",
        "parsed_plan": plan
    }


# ----------------------------------------------------------------
# Validation Conditions
# ----------------------------------------------------------------

def validate_resolution_blankField(content, required_keys):

    if isinstance(content, str):
        content = json.loads(content)

    validation = {
        key: (
            content.get(key) is not None
            and str(content.get(key)).strip() != ""
        )
        for key in required_keys
    }

    return {
        "validation_passed": all(validation.values()),
        "details": validation
    }


# -----------------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------------

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
        func=validate_resolution_blankField
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