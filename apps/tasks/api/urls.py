from django.urls import path
from . import views

urlpatterns = [
    path('create-comment/', views.CommentCreateAPIView.as_view()),
    path('list-comment/', views.CommentListAPIView.as_view()),
    path('rud-comment/<int:pk>/', views.CommentRUDAPIView.as_view()),
    path('create-task/', views.TaskCreateAPIView.as_view()),
    path('list-tasks/', views.TaskListAPIView.as_view()),
    path('task-detail/<int:pk>/', views.TaskRetrieveAPIView.as_view()),
    path('send-task/', views.SendTaskCreateAPIView.as_view()),
    path('recieve-task/', views.SendTaskAPIView.as_view()),
    path('destroy-task/<int:pk>/', views.TaskDestroyAPIView.as_view()),
    path('task-update/<int:pk>/', views.TaskUpdateAPIView.as_view()),

]
