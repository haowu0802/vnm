#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import uuid
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

class Actor(models.Model):
    name = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='actors', null=True)
    thumb = ImageSpecField(source='avatar',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 90})
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ActorImage(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    thumb = ImageSpecField(source='image',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 50})
    actor = models.ForeignKey('actor', on_delete=models.PROTECT, null=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=1768)
    height = models.IntegerField(default=992)
    filename = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.filename}'