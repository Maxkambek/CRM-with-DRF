from django.urls import path
from .views import TodoListCreateAPIView, TodoListAPIView, TodoRUDAPIView

urlpatterns = [
    path('', TodoListCreateAPIView.as_view()),
    path('list/', TodoListAPIView.as_view()),
    path('rud/<int:pk>/', TodoRUDAPIView.as_view())
]
