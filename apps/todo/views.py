from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework import generics
from rest_framework import permissions as p
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer
from apps.accounts import permissions


class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsOwnerOrReadOnlyForAccount]


class TodoListAPIView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        # qs = super().get_queryset().filter(owner=self.request.user)
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        month = self.request.GET.get('month')
        if month:
            qs = qs.filter(created_at__month=month)
        if search:
            qs = qs.filter(title__icontains=search)
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)

        return qs

    def filter_qs(self, val):
        qs = self.get_queryset().filter(created_at__contains=val)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        lst = qs.annotate(date=TruncDay('created_at')).annotate(count=Count('id')).values('date')
        data = {
            'count': lst.count(),
            'results': []
        }

        for i in lst:
            data['results'].append({
                'date': i.get('date'),
                'count': i.get('count'),
                'todo': [{'id': j.id, 'title': j.title} for j in self.filter_qs(i.get('date'))]
            })

        return Response(data)


class TodoListSortByDeadlineAPIView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def filter_qs(self,val):
        qs = self.get_queryset().filter(deadline__contains=val)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        lst = qs.annotate(date=TruncDay('deadline')).annotate(count=Count('id')).values('date')
        data = {
            'count': lst.count(),
            'results': []
        }

        for i in lst:
            data['results'].append({
                'date': i.get('date'),
                'count': i.get('count'),
                'todo': [{'id': j.id, 'title': j.title} for j in self.filter_qs(i.get('date'))]
            })

        return Response(data)


class TodoRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'
    permission_classes = [p.IsAuthenticated]
