from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'passwords', PasswordsViewSet, basename='password')



urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIVIew.as_view(), name='logout'),
    path('auth-status/', AuthStatuAPIView.as_view(), name='auth-status'),
    path('get-passowords/', UsersPasswordsAPIView.as_view(), name='get-passwords'),
    path('save-password/', SavePasswordAPIView.as_view(), name='save-password'),
    path('delete-password/', DeletePasswordAPIView.as_view(), name='delete-password'),
]
