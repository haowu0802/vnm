#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import uuid
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

class Actor(models.Model):
    name = models.CharField(max_length=70)
    avatar = models.ImageField(upload_to='actors')
    thumb = ImageSpecField(source='avatar',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 90})
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

class ActorImage(models.Model):
    image = ProcessedImageField(upload_to='images',
        processors=[ResizeToFill(1768, 992)],
        format='JPEG',
        options={'quality': 100})
    thumb = ImageSpecField(source='image',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 90})
    actor = models.ForeignKey('actor', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=1768)
    height = models.IntegerField(default=992)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)