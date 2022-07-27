import jwt
from django.contrib.auth import logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from drf_yasg import openapi
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from config import settings
from .permissions import IsOwnerOrReadOnlyForAccount
from .serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer, ResetPasswordSerializer, \
    SetNewPasswordSerializer, AccountSerializer, TeamSerializer
from .models import Account, Team
from .utils import Util
from ..tasks.permissions import IsAdminUser


class UserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = Account.objects.filter(email=user_data['email']).first()
        token = RefreshToken.for_user(user)

        current_site = 'localhost:8000'
        relative_link = '/accounts/verify-email/'
        abs_url = 'http://' + current_site + relative_link + '?token=' + str(token.access_token)
        email_body = f'Hi, {user.email} \n Use link below to verify your email\n {abs_url}'
        data = {
            'to_email': user.email,
            'email_subject': 'Verify email desk',
            'email_body': email_body
        }
        Util.send_email(data)

        return Response({'success': True, 'message': 'Activate url was sent'}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify email',
                                           type=openapi.TYPE_STRING)

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = Account.objects.filter(id=payload['user_id']).first()
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'success': True, 'message': 'Email successfully verified'})
        except jwt.ExpiredSignatureError as e:
            return Response({'success': False, 'message': f'Verification expired | {e.args}'})
        except jwt.exceptions.DecodeError as e:
            return Response({'success': False, 'message': f'Invalid token | {e.args}'})


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        user = Account.objects.filter(email=request.data['email']).first()

        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = 'localhost:8000'
            abs_url = f'http://{current_site}/set-password-confirm?uidb64={uidb64}&?token={token}'
            email_body = f'Hi, {user.email} \n Use link below to verify your email\n {abs_url}'
            data = {
                'to_email': user.email,
                'email_subject': 'Verify email desk',
                'email_body': email_body
            }
            Util.send_email(data)
            return Response({'success': True, 'message': 'Send link to email'})
        return Response({'success': False, 'message': 'Email not match'})


class PasswordTokenCheckView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        uidb64 = request.GET.get('uidb64')
        token = request.GET.get('token')
        try:
            id = smart_str(urlsafe_base64_encode(uidb64))
            user = Account.objects.filter(id=id).first()
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': False, 'message': 'Token is not valid'})
        except DjangoUnicodeDecodeError as e:
            return Response({'success': False, 'message': f'Token is not valid | {e.args}'})
        return Response({'success': True, 'message': 'Successfully checked', 'uidb64': uidb64, 'token': token})


class SetPasswordCompletedView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'message': 'Successfully set new password'})
        return Response({"success": False, 'message': 'Credentials is invalid'})


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyAccountAPIView(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerOrReadOnlyForAccount]
    lookup_field = 'email'


class AccountListAPIView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AddTeamAPIView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAdminUser]


class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]
