from django.urls import path

from rest_framework import routers
from .views import TaskViewSet


router = routers.SimpleRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = []
urlpatterns += router.urls
