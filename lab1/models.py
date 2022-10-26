from django.db import models


class Films(models.Model):
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
