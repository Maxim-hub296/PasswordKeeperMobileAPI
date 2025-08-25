from .views import *
from django.urls import path

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration')
]
