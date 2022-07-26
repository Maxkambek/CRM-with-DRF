from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from ..models import Task, SendTask, Comment
from . import serializers
from ...accounts.permissions import IsOwnerOrReadOnlyForAccount
from ..permissions import IsAdminUser


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = serializers.CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(task_id=q)
        return qs


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAdminUser]


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(is_deleted=False)
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        if search:
            qs = qs.filter(title__icontains=search)
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)

        return qs


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class TaskDestroyAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True


class TaskUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]


class SendTaskCreateAPIView(generics.CreateAPIView):
    queryset = SendTask.objects.all()
    serializer_class = serializers.SendTaskSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(sender=user)


class SendTaskAPIView(generics.ListAPIView):
    queryset = SendTask.objects.all()
    serializer_class = serializers.SendTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(receiver_id=self.request.user.id)
        return qs
