import logging

log = logging.getLogger(__name__)

TASK_TO_STEP_STATE = {
    "running": "running",
    "complete": "success"
    # etc
}

def get_task_group_state(taskGroupId):
    # TODO query taskcluster group api for overall state
    # return summary of remaining tasks and tasks that have failed while exhausting retries
    pass