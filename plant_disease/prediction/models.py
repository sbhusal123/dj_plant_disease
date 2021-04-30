from django.db import models


class Disease(models.Model):
    name = models.CharField(max_length=80, unique=True, blank=False)
    description = models.TextField(blank=True, null=True)
    medicine = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name
