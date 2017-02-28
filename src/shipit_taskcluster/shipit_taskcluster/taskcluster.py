
TASK_TO_STEP_STATE = {
    "running": "running",
    "complete": "success"
    # etc
}

def get_task(taskGroupId, taskid):
    # return taskid and ensure it is in taskGroupId
    pass

def create_task_group():
    # return taskGroupId and ensure it is in taskGroupId
    pass

def get_task_group_state(taskGroupId):
    # query taskcluster group api for overall state
    pass

def cancel_tasks(taskGroupId):
    # cancel all tasks by taskGroupId
    pass

def cancel_task(taskId):
    # cancel task by taskId
    pass

def update_task_state(taskId, result):
    # force task result
    pass
