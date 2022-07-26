from rest_framework import serializers
from ..models import Notification, Chat
from ...accounts.serializers import AccountSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'description',
            'user',
            'is_read',
            'created_at'
        ]


class NotificationListSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'description',
            'user',
            'is_read',
            'created_at'
        ]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            'id',
            'sender',
            'receiver',
            'message',
            'created_at',
            'updated_at',
            'is_deleted',
        ]


class ChatListSerializer(serializers.ModelSerializer):
    sender = AccountSerializer()
    receiver = AccountSerializer()

    class Meta:
        model = Chat
        fields = [
            'id',
            'sender',
            'receiver',
            'message',
            'created_at',
            'updated_at',
            'is_deleted',
        ]
