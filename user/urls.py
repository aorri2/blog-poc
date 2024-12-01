from django.urls import path

from .views import LoginView, SignupView

app_name = "user"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="user_signup"),
    path("login/", LoginView.as_view(), name="login"),
]
