#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import uuid
import zipfile
import django_photo_gallery.settings
from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.core.files.base import ContentFile

from PIL import Image

from app.models import Actor, ActorImage
from app.forms import ActorForm

@admin.register(Actor)
class ActorModelAdmin(admin.ModelAdmin):
    form = ActorForm
    #list_display = ('name', 'thumb')
    #list_filter = ('created',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            actor = form.save(commit=False)
            actor.modified = datetime.now()
            actor.save()

# In case image should be removed from Actor.
@admin.register(ActorImage)
class ActorImageModelAdmin(admin.ModelAdmin):
    #list_display = ('actor', )
    #list_filter = ('actor', 'created')
    pass