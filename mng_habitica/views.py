import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mng_habitica.handlers.commands import task_compleeted


def index(request):
    return JsonResponse({"error": "sup hacker"})


@csrf_exempt
def mng(request):
    if request.method == "POST":
        json_string = request.body.decode('utf-8').replace('_id', 'id')
        task_compleeted(json.loads(json_string))
        return JsonResponse({"ok": "POST request processed"})
