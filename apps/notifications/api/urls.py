from django.urls import path
from . import views

urlpatterns = [
    path('chat-list/', views.ChatListAPIView.as_view()),
    path('chat-create/', views.ChatCreateAPIView.as_view()),
    path('notification-list/', views.NotificationListAPIView.as_view()),
    path('notification-create/', views.NotificationCreateAPIView.as_view())
]
