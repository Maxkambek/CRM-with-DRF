from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('verify-email/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('reset-password/', views.ResetPasswordView.as_view()),
    path('set-password-confirm/', views.PasswordTokenCheckView.as_view()),
    path('set-password-completed/', views.SetPasswordCompletedView.as_view()),
    path('profile/<str:email>/', views.MyAccountAPIView.as_view()),
    path('create-team/', views.AddTeamAPIView.as_view()),
    path('users-list/', views.AccountListAPIView.as_view()),
    path('team-list/', views.TeamListAPIView.as_view()),
    # path('delete-team/<int:pk>/', views.DestroyTeamAPIView.as_view()),
    path('rud-team/<int:pk>/', views.TeamRUDAPIView.as_view()),
]
