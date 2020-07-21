from django.db import models

class Novel(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d')