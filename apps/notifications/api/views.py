from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from ..models import Notification, Chat
from .serializers import NotificationSerializer, NotificationListSerializer, ChatListSerializer, ChatSerializer
from apps.tasks.permissions import IsAdminUser


class NotificationCreateAPIView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]


class NotificationListAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(is_read=False)
        qs = qs.order_by('-id')
        return qs


class ChatCreateAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        sender = self.request.user
        serializer.save(sender=sender)


class ChatListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(is_deleted=False).order_by('-id')
        qs = qs.filter(Q(reciever_id=self.request.user.id) | Q(sender_id=self.request.id))
        return qs
