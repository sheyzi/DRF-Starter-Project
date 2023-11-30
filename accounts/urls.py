from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    path("me/", views.MeUpdateRetrieveView.as_view(), name="me"),
    path("user_exists/", views.UserExistsView.as_view(), name="user_exists"),
    path("setup-admin/", views.SetupView.as_view(), name="setup_admin"),
    path(
        "login/", views.DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("refresh/", views.DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", views.DecoratedTokenVerifyView.as_view(), name="token_verify"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "password-reset/",
        views.ResetPasswordRequestTokenView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/confirm/",
        views.ResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/validate_token/",
        views.ResetPasswordValidateTokenView.as_view(),
        name="password_reset_validate_token",
    ),
    path("users/", views.ListAccountsView.as_view(), name="users"),
    path("users/<int:id>/", views.RetrieveUpdateAccountView.as_view(), name="user"),
    path("users/change-password/", views.ChangePasswordView.as_view(), name="user"),
    path("groups/", views.CreateListGroupView.as_view(), name="group"),
    path(
        "groups/<int:id>/", views.RetrieveUpdateDestroyGroupView.as_view(), name="group"
    ),
    path("permissions/", views.ListPermissionView.as_view(), name="permissions"),
]
