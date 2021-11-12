#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import uuid
import os
from pathlib import Path

from django.db import models

from imagekit import ImageSpec
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(300, 300)]
    format = 'JPEG'
    options = {'quality': 60}


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


class Story(models.Model):
    name = models.CharField(max_length=128)
    actor = models.ForeignKey('actor', on_delete=models.CASCADE, null=True)
    thumb = models.ImageField(upload_to='thumb', null=True)
    filepath = models.CharField(max_length=1024, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['filepath']

    def __str__(self):
        return f"{self.actor.name} - {self.name}" 


class ActorImage(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    thumb = ImageSpecField(source='image',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 50})
    actor = models.ForeignKey('actor', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=1768)
    height = models.IntegerField(default=992)
    filename = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.filename}'


class ActorImageLocal(models.Model):
    thumb = models.ImageField(upload_to='thumb', null=True)
    story = models.ForeignKey('story', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=1768)
    height = models.IntegerField(default=992)
    filepath = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ['filepath']

    def __str__(self):
        return f'{self.filepath}'

    def is_video(self):
        ext = Path(self.filepath).suffix
        # video file skip dimentions
        if ext in ['.mp4']:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        # check empty and generate thumbnail from original image file
        if not self.thumb and not self.is_video():
            print(f"Generating thumbnail for - {self.filepath} ")
            source_file = open(self.filepath, 'rb')
            image_generator = Thumbnail(source=source_file)
            result = image_generator.generate()
            self.thumb.save(
                os.path.join('tmp', os.path.basename(self.filepath)), 
                result,
            )
            print(f"Thumbnail generated - {self.thumb}")
            # populate story thumb
            if not self.story.thumb:
                self.story.thumb = self.thumb
                self.story.save()
            return
        super(ActorImageLocal, self).save(*args, **kwargs)