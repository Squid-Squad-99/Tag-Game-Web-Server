from django.urls import path, include
from . import views

urlpatterns = [
    path(r'signup/', views.signup, name="signup"),
    path(r'signup/sucess/', views.signup_success, name="signup-success"),
]