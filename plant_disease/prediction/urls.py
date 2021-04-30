from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import PredictView, LoginView, UserRegistrationView
urlpatterns = [
    # Auth views
    path('', LoginView.as_view(), name="login"),
    path('register', UserRegistrationView.as_view(), name="register"),
    path('logout', LogoutView.as_view(), name="logout"),

    # Custom views
    path('predict', PredictView.as_view(), name="predict"),
]
