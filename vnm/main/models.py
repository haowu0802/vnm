from django.db import models
from django.utils.html import mark_safe

class Novel(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d')

    def __str__(self):
        return self.title or self.file.name


class Actor(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    file = models.ImageField(upload_to='images', blank=True)
    actor = models.ForeignKey(Actor, related_name='images', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='tags', blank=True)

    def __str__(self):
        return self.file.url

    def image_tag(self):
            return mark_safe('<img src="/media/%s" width="100" height="100" />' % (self.file))

    image_tag.short_description = 'Image'


class Matcher(models.Model):
    match = models.CharField(max_length=256)
    prefix = models.CharField(max_length=256, blank=True, null=True)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)

    def __str__(self):
        return self.match

class Tag(models.Model):
    name = models.CharField(max_length=256)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name