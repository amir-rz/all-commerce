from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView
app_name = "user"

urlpatterns = [
    path("signup/", views.SignupUserView.as_view(), name="signup"),
    path("request-vcode/", views.RequestVCodeView.as_view(), name="request-vcode"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("verify-phone-number/", views.VerifyNewPhoneNumberView.as_view(),
         name="verify-phone-number"),

    path("obtain-token/", views.ObtainToken.as_view(), name="obtain-token"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),


]
