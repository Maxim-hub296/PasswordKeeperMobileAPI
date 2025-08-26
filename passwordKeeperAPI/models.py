from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Password(models.Model):
    site_name = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password_text = models.CharField(max_length=500)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')


    def __str__(self):
        return f'Пароль пользователя {self.user} к сайту {self.site_name}'