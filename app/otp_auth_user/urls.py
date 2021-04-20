from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("signup/", views.SignupUserView.as_view(), name="signup"),
    path("request-vcode/", views.RequestVCodeView.as_view(), name="request-vcode"),
    path("signin/", views.SigninUserView.as_view(), name="signin"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("verify-phone-number/", views.VerifyNewPhoneNumber.as_view(),
         name="verify-phone-number")

]
