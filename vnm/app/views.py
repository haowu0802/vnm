#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from os import listdir
from os.path import isfile, join, getmtime, basename

from PIL import Image

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.core.files import File
from django.core.files.images import ImageFile

from app.models import Actor, ActorImage, ActorImageLocal, Story


def create_image(story, filepath):
    if not ActorImageLocal.objects.filter(filepath=filepath).exists():
        # get image dim
        im = Image.open(filepath)
        width, height = im.size
        # instantiate
        photo = ActorImageLocal(
            filepath=filepath,
            story=story,
            width=width,
            height=height,
            created=getmtime(filepath),
        )
        photo.save()


def image(request, image_id):
    file = get_object_or_404(ActorImageLocal, pk=image_id)
    img = open(file.filepath, 'rb')
    response = FileResponse(img)
    return response


def actors(request):
    """loads list of available image sets from a local path
    """
    actor_list = [f for f in listdir(settings.LOCAL_PATH) if not isfile(join(settings.LOCAL_PATH, f))]
    return render(request, 'actors.twig', { 'actors': actor_list })


# local image listing view
def actor(request, name):
    # create actor if not exist
    act, created = Actor.objects.get_or_create(
        name=name,
    )
    if created:
        act = Actor.objects.get(name=name)

    # get local image path from settings and fetch file list
    dir_path = join(settings.LOCAL_PATH, name)
    dir_list = [f for f in listdir(dir_path) if not isfile(join(dir_path, f))]

    # create story objects
    for storyname in dir_list:
        filepath = join(dir_path, storyname)
        if not Story.objects.filter(filepath=filepath).exists():
            story = Story(
                name=storyname,
                filepath=filepath,
                actor=act,
                created=getmtime(filepath),
            )
            story.save()

    story_list = Story.objects.filter(actor=act).all()
    return render(request, 'stories.twig', { 'stories': story_list })


def story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    # get local image path from settings and fetch file list
    dir_path = story.filepath
    file_list = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    for filename in file_list:
        filepath = join(dir_path, filename)
        create_image(story, filepath)

    images = ActorImageLocal.objects.filter(story=story)

    # ordering
    sort = request.GET.get('sort')

    if sort:
        images = images.order_by(sort),
        images = images[0]

    return render(request, 'actor.twig', {
        'story': story,
        'images': images,
    })


class ActorDetail(DetailView):
     model = Actor

     def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ActorDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = ActorImage.objects.filter(actor=self.object.id)
        return context

def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)