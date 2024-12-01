from django.urls import path

from .views import SignupView

app_name = "user"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="user_signup"),
]
