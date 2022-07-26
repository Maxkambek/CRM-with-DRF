from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from apps.accounts.models import Account, Team


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=4, write_only=True)
    password2 = serializers.CharField(max_length=64, min_length=4, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'email', 'image', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password not match'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=111, required=True)
    password = serializers.CharField(max_length=64, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        user = Account.objects.filter(email=obj.get("email")).first()
        return user.tokens

    class Meta:
        model = Account
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise
        if not user.is_active:
            raise

        data = {
            'success': True,
            'email': user.email,
            'tokens': user.tokens
        }
        return data


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ['token']


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Account
        fields = ('email',)


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=64)
    password2 = serializers.CharField(min_length=6, max_length=64)
    uidb64 = serializers.CharField(max_length=64, required=True)
    token = serializers.CharField(max_length=555, required=True)

    class Meta:
        model = Account
        fields = ['password', 'password2', 'uidb64', 'token']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        _id = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.filter(id=_id).first()

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed({'success': False, 'message': 'The token is invalid'})
        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password not match'})

        user.set_password(password)
        user.save()
        return user


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'first_name', 'last_name', 'image', 'bio', 'is_staff', 'is_active', 'is_supervisor',
                  'is_admin', 'date_login']


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'user', 'supervisor', 'name', 'get_count']
        extra_kwargs = {
            'get_count': {'read_only': True}
        }
