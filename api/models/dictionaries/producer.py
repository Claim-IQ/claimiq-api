from django.db import models


class Producer(models.Model):
    """Producer model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
