
import json
from collections import namedtuple

json_data = '{"success":true,"data":{"challenge":{},"group":{"approval":{"required":false,"approved":false,"requested":false},"assignedUsers":[],"sharedCompletion":"singleCompletion"},"completed":false,"collapseChecklist":false,"type":"todo","notes":"","tags":[],"value":0,"priority":1,"attribute":"str","byHabitica":false,"text":"dfgndfnfgndfgn","checklist":[],"reminders":[],"_id":"ce446f65-0f7d-42d1-868e-018018357233","createdAt":"2021-06-11T18:37:13.543Z","updatedAt":"2021-06-11T18:37:13.543Z","userId":"3762f4b8-b058-40d4-bfcb-3b0e71a6a831","id":"ce446f65-0f7d-42d1-868e-018018357233"},"notifications":[{"type":"CRON","data":{"hp":0,"mp":10},"seen":false,"id":"59cfe2af-47ce-48c5-8ea6-e4c8cd68e162"}],"userV":129,"appVersion":"4.196.1"}'

json_data = json_data.replace('_id', 'id')
obj = json.loads(json_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

kek = {'qwer':'qwer'}
print(obj)

# Task.task_update_or_create(obj)