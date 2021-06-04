from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
  ratings = models.CharField(max_length=10000, blank=True)

  def get_absolute_url(self):
    return reverse('user_detail', args=[str(self.id)])
