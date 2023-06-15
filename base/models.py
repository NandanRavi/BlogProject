from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    def __str__(self):
        return str(self.title)