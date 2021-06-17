import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from manager1c.handlers.commands import process_1c_event


@csrf_exempt
def msg(request):
    if request.method == "POST":
        print(request.body)
        process_1c_event(json.loads(request.body))
        return JsonResponse({"200": "POST request processed"})
