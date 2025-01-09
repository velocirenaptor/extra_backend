from django.db import models
from django.conf import settings

#create new model with 4 fields > point 1
class Character(models.Model):
    name = models.TextField(blank=True)
    source = models.TextField(blank=True)
    picture = models.URLField()
    description = models.TextField(blank=True)

    class Meta:
        db_table = "characters"

    def __str__(self):
        return self.title