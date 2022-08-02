from django.db import models
from .models import User


def set_username(sender, instance, **kwargs):
    username = instance.first_name
    counter = 1
    while User.objects.filter(username=username):
        username = instance.first_name + str(counter)
        counter += 1
    instance.username = username


models.signals.pre_save.connect(set_username, sender=User)
