from django.contrib.auth.models import Group, Permission
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

from cfehome.serializers import MessageSerializer, StatusSerializer
from cfehome.utils import Util
from .models import Account, BlacklistedToken
from .serializers import (
    RegisterAccountSerializer,
    AccountSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
    UserExistsMessageSerializer,
    GroupSerializer,
    PermissionSerializer,
    ChangePasswordSerializer,
    ResendVerificationEmailSerializer,
    VerifyEmailSerializer,
)
from cfehome.permissions import IsEntityManager

from django_rest_passwordreset.views import (
    ResetPasswordConfirm,
    ResetPasswordValidateToken,
    ResetPasswordRequestToken,
)
from .signals import send_verification_mail


class DecoratedTokenObtainPairView(TokenObtainPairView):
    api_tags = ["Authentication"]
    api_operation_id = "get_auth_tokens"

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
        operation_summary="Get JWT tokens",
        operation_description="Returns a pait of JWT tokens when valid credentials are provided.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    api_tags = ["Authentication"]
    api_operation_id = "refresh_auth_tokens"

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        },
        operation_summary="Refresh JWT tokens",
        operation_description="Returns a new pair of JWT tokens when valid refresh token is provided.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    api_tags = ["Authentication"]
    api_operation_id = "verify_jwt_tokens"

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        },
        operation_summary="Verify JWT tokens",
        operation_description="Returns a 200 OK response when valid a valid access or refresh token is provided. If the token is invalid, expired or blacklisted, a 401 Unauthorized response is returned.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AdminExistsView(generics.GenericAPIView):
    api_tags = ["User"]
    api_operation_id = "check_if_user_exists"
    api_summary = "Check if user exists"
    api_description = "Checks if a user exists in the database."
    filter_backends = []

    serializer_class = UserExistsMessageSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: UserExistsMessageSerializer,
        },
    )
    def get(reqests, *args, **kwargs):
        admin = Account.objects.first()

        if admin:
            return Response(
                UserExistsMessageSerializer(
                    {"message": "Admin exists", "exists": True}
                ).data
            )
        else:
            return Response(
                UserExistsMessageSerializer(
                    {"message": "No admin exists", "exists": False}
                ).data
            )


class SetupAdminView(generics.CreateAPIView):
    api_tags = ["User"]
    api_operation_id = "setup_user"
    api_summary = "Setup first superuser"
    api_description = "Creates the first superuser in the database. This endpoint is only available if no admin exists in the database."

    serializer_class = RegisterAccountSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        admin = Account.objects.filter(is_superuser=True).first()

        if admin:
            return Response(
                MessageSerializer({"message": "Admin already exists"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validate(data=request.data)

            del validated_data["password2"]
            admin = Account.objects.create_superuser(**validated_data)
            serializer = self.serializer_class(admin)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MeUpdateRetrieveView(generics.RetrieveUpdateAPIView):
    """
    Returns the current user's information.

    This endpoint requires authentication.
    """

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    api_tags = ["User"]

    @swagger_auto_schema(
        operation_id="get_current_user",
        operation_summary="Get current user information",
        operation_description="Returns the current user's information.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="partially_update_current_user",
        operation_summary="Partially update current user information",
        operation_description="Partially updates the current user's information.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="update_current_user",
        operation_summary="Update current user information",
        operation_description="Updates the current user's information.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    """
    Register a new user.

    This endpoint creates a new user in the database, it doesn't require authentication.
    """

    serializer_class = RegisterAccountSerializer
    permission_classes = [permissions.AllowAny]

    api_tags = ["User"]
    api_operation_id = "register_user"

    @swagger_auto_schema(
        operation_summary="Register user",
        operation_description="Registers a new user.",
        operation_id="register_user",
    )
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validate(data=request.data)

            del validated_data["password2"]
            user = Account.objects.create_user(**validated_data)
            send_verification_mail.send(sender=self.__class__, instance=self, user=user)

            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResendVerificationEmailView(generics.GenericAPIView):
    serializer_class = ResendVerificationEmailSerializer
    permission_classes = [permissions.AllowAny]

    api_tags = ["User"]
    api_operation_id = "resend_verification_email"
    api_summary = "Resend verification email"
    api_description = "Resends the email verification email to the user."

    @swagger_auto_schema(
        operation_summary="Resend verification email",
        operation_description="Resends the email verification email to the user.",
        operation_id="resend_verification_email",
        responses={
            status.HTTP_200_OK: MessageSerializer,
            status.HTTP_400_BAD_REQUEST: MessageSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = Account.objects.get(email=data["email"])

            if user.email_verified:
                return Response(
                    MessageSerializer({"message": "Email already verified"}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            send_verification_mail.send(sender=self.__class__, instance=self, user=user)

            return Response(
                MessageSerializer(
                    {"message": "Verification email sent successfully"}
                ).data,
                status=status.HTTP_200_OK,
            )


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [permissions.AllowAny]

    api_tags = ["User"]
    api_operation_id = "verify_email"
    api_summary = "Verify email"
    api_description = "Verifies the user's email."

    @swagger_auto_schema(
        operation_summary="Verify email",
        operation_description="Verifies the user's email.",
        operation_id="verify_email",
        responses={
            status.HTTP_200_OK: MessageSerializer,
            status.HTTP_400_BAD_REQUEST: MessageSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            token = data["token"]

            payload = Util.validate_verification_token(token)

            if not payload:
                return Response(
                    MessageSerializer({"message": "Invalid token"}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = Account.objects.get(id=payload["user_id"])

            BlacklistedToken.objects.create(token=token)

            if user.email_verified:
                return Response(
                    MessageSerializer({"message": "Email already verified"}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.email_verified = True
            user.save()

            return Response(
                MessageSerializer({"message": "Email verified successfully"}).data,
                status=status.HTTP_200_OK,
            )


class ListAccountsView(generics.ListAPIView):
    """
    Returns a list of all users.

    Only staff users with the `accounts.view_account` permission can access this view.
    """

    serializer_class = AccountSerializer

    permission_classes = [IsEntityManager]
    queryset = serializer_class.Meta.model.objects.all().order_by("-date_joined")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["email", "first_name", "last_name"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["email", "first_name", "last_name"]

    api_tags = ["User"]
    api_operation_id = "list_users"


class RetrieveUpdateAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer

    permission_classes = [IsEntityManager]
    queryset = serializer_class.Meta.model.objects.all()
    lookup_field = "id"

    api_tags = ["User"]

    @swagger_auto_schema(
        operation_summary="Get user information",
        operation_description="Returns the user's information.",
        operation_id="get_user",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update user information",
        operation_description="Updates the user's information.",
        operation_id="update_user",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update user information",
        operation_description="Partially updates the user's information.",
        operation_id="partially_update_user",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CreateListGroupView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsEntityManager]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    queryset = Group.objects.all()

    api_tags = ["Groups"]

    @swagger_auto_schema(
        operation_summary="Create group",
        operation_description="Creates a new group.",
        operation_id="create_group",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="List groups",
        operation_description="Returns a list of all groups.",
        operation_id="list_groups",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListPermissionView(generics.ListAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [IsEntityManager]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "codename"]
    search_fields = ["name", "codename"]
    ordering_fields = ["name", "codename"]
    queryset = Permission.objects.all()

    api_tags = ["Permissions"]
    api_operation_id = "list_permissions"
    api_summary = "List permissions"
    api_description = "Returns a list of all permissions."


class RetrieveUpdateDestroyGroupView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsEntityManager]

    lookup_field = "id"
    queryset = Group.objects.all()

    api_tags = ["Groups"]

    @swagger_auto_schema(
        operation_summary="Get group information",
        operation_description="Returns the group's information.",
        operation_id="get_group",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update group information",
        operation_description="Updates the group's information.",
        operation_id="update_group",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update group information",
        operation_description="Partially updates the group's information.",
        operation_id="partially_update_group",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete group",
        operation_description="Deletes the group.",
        operation_id="delete_group",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    api_tags = ["User"]
    api_operation_id = "change_password"
    api_summary = "Change current user's password"
    api_description = "Changes the current user's password."

    @swagger_auto_schema(
        operation_summary="Change password",
        operation_description="Changes the current user's password.",
        operation_id="change_password",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validate(data=request.data)

            user = self.request.user
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(validated_data["new_password"])
                user.save()
                update_session_auth_hash(request, user)

                return Response(
                    MessageSerializer(
                        {"message": "Password changed successfully"}
                    ).data,
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"old_password": ["Incorrect old password"]},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordValidateTokenView(ResetPasswordValidateToken):
    api_tags = ["Authentication"]
    api_operation_id = "validate_password_reset_token"

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: StatusSerializer,
        },
        operation_summary="Validate password reset token",
        operation_description="Validates a password reset token.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)  # pragma: no cover


class ForgotPasswordView(ResetPasswordRequestToken):
    api_tags = ["Authentication"]
    api_operation_id = "forgot_password"

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: StatusSerializer,
        },
        operation_summary="Forgot password",
        operation_description="Sends a password reset token to the user if they are registered.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)  # pragma: no cover


class ResetPasswordView(ResetPasswordConfirm):
    api_tags = ["Authentication"]
    api_operation_id = "reset_password"

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: StatusSerializer,
        },
        operation_summary="Reset password",
        operation_description="Changes the user's password.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)  # pragma: no cover
