# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import logging
import collections

from shipit_taskcluster.taskcluster import get_task, create_task_group, cancel_tasks, cancel_task
from shipit_taskcluster.taskcluster import get_task_group_state, TASK_TO_STEP_STATE
from shipit_taskcluster.taskcluster import update_task_state

log = logging.getLogger(__name__)

STEPS = {}
STEP = collections.namedtuple("Step", "uid state taskGroupId")


## api

def list_steps():
    log.info('listing steps')
    return STEPS.keys()

def query_state(step):
    return TASK_TO_STEP_STATE[get_task_group_state(step.taskGroupId)]


def get_step(uid):
    log.info('getting step %s', uid)
    if not STEPS.get(uid):
        return "Step with uid {} unknown".format(uid), 404
    step = STEPS[uid]
    return dict(uid=step.uid, input={}, parameters=step)


def get_step_status(uid):
    log.info('getting step status %s', uid)
    if not STEPS.get(uid):
        return "Step with uid {} unknown".format(uid), 404
    step = STEPS[uid]
    step.state = query_state(step)
    return dict(
        state=step.state
    )


def create_step(uid, inputs):
    log.info('creating step %s', uid)
    taskGroupId = create_task_group(inputs)
    STEPS[uid] = STEP(uid=uid, state='running', taskGroupId=taskGroupId)
    return None


def delete_step(uid):
    log.info('deleting step %s', uid)
    if not STEPS.get(uid):
        return "step with uid {} unknown".format(uid), 404
    cancel_tasks(STEPS[uid].taskGroupId)
    del STEPS[uid]
    return None


def rerun_task(uid, taskid):
    log.info('rerunning task %s', taskid)
    if not STEPS.get(uid):
        return "step with uid {} unknown".format(uid), 404
    taskid = get_task(STEPS[uid]['taskGroupId'], taskid)
    if not taskid:
        return "task with taskid {} unknown".format(taskid), 404
    STEPS[uid].state = 'running'
    return None


def report_task_complete(uid, taskid):
    log.info('rerunning task %s', taskid)
    if not STEPS.get(uid):
        return "Step with uid {} unknown".format(uid), 404
    taskid = get_task(STEPS[uid]['taskGroupId'], taskid)
    if not taskid:
        return "task with taskid {} unknown".format(taskid), 404
    return update_task_result(taskid, 'complete')


def cancel_task(uid, taskid):
    log.info('force cancelling task %s', taskid)
    if not STEPS.get(uid):
        return "Step with uid {} unknown".format(uid), 404
    taskid = get_task(STEPS[uid]['taskGroupId'], taskid)
    if not taskid:
        return "task with taskid {} unknown".format(taskid), 404
    return cancel_task(taskid)


def cancel_task_group(uid):
    log.info('creating graph %s', uid)
    if not STEPS.get(uid):
        return "Step with uid {} unknown".format(uid), 404
    return cancel_tasks(STEPS[uid].taskGroupId)
