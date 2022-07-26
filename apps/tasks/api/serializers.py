from rest_framework import serializers
from ..models import Task, SendTask, Comment
from ...accounts.models import Account
from ...accounts.serializers import AccountSerializer


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'message', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'status', 'type', 'created_at', 'updated_at', 'description', 'supervisor',
                  'deadline', 'is_deleted', 'description']


class CommentSerializer(serializers.ModelSerializer):
    user = AccountSerializer()
    task = TaskSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'message', 'created_at']


class SendTaskSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(max_length=222, read_only=True)

    class Meta:
        model = SendTask
        fields = ['id', 'task', 'sender', 'receiver', 'team', 'created_at']
        extra_kwargs = {
            'sender': {'required': False}
        }
