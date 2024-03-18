from django.db import models
from django.contrib.auth.models import User

class Relay(models.Model):
    mac_addr = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    state = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.mac_addr
