from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TaskSerializer
from ..models import Task


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.filter(completed=False)
    serializer_class = TaskSerializer