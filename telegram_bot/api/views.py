from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TaskSerializer, AnimeSerializer
from ..models import Task, User
from ..handlers.anime import search


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.filter()
    serializer_class = TaskSerializer

