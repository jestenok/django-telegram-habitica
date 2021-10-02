from rest_framework import serializers

from ..models import Task, User, Anime


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    user_telegram_id = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class AnimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Anime
        fields = '__all__'