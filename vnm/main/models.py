from django.db import models

class Novel(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d')

    def __str__(self):
        return self.title or self.file.name


class Actor(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Matcher(models.Model):
    match = models.CharField(max_length=256)
    prefix = models.CharField(max_length=256, blank=True, null=True)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)

    def __str__(self):
        return self.match