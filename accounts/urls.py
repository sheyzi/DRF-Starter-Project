from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    path("me/", views.MeUpdateRetrieveView.as_view(), name="me"),
    path("user_exists/", views.AdminExistsView.as_view(), name="admin_exists"),
    path("setup-admin/", views.SetupAdminView.as_view(), name="setup_admin"),
    path("login/", views.DecoratedTokenObtainPairView.as_view(), name="login"),
    path("refresh/", views.DecoratedTokenRefreshView.as_view(), name="refresh"),
    path("verify/", views.DecoratedTokenVerifyView.as_view(), name="verify_token"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "forgot-password/",
        views.ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "reset-password/",
        views.ResetPasswordView.as_view(),
        name="reset_password",
    ),
    path(
        "reset-password/validate_token/",
        views.ResetPasswordValidateTokenView.as_view(),
        name="validate_reset_password_token",
    ),
    path("users/", views.ListAccountsView.as_view(), name="list_users"),
    path(
        "users/<int:id>/",
        views.RetrieveUpdateAccountView.as_view(),
        name="retrieve_user",
    ),
    path(
        "users/change-password/",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("groups/", views.CreateListGroupView.as_view(), name="list_groups"),
    path(
        "groups/<int:id>/",
        views.RetrieveUpdateDestroyGroupView.as_view(),
        name="retrieve_group",
    ),
    path("permissions/", views.ListPermissionView.as_view(), name="list_permissions"),
]
