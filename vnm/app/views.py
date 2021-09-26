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

from app.models import Actor, ActorImage, ActorImageLocal


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
    file_list = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    # create image objects
    for filename in file_list:
        filepath = join(dir_path, filename)

        if not ActorImageLocal.objects.filter(filepath=filepath).exists():
            # get image dim
            im = Image.open(filepath)
            width, height = im.size
            # instantiate
            photo = ActorImageLocal(
                filepath=filepath,
                actor=act,
                width=width,
                height=height,
                created=getmtime(filepath),
            )
            photo.save()

    images = ActorImageLocal.objects.filter(actor=act)

    # ordering
    sort = request.GET.get('sort')

    if sort:
        images = images.order_by(sort),
        images = images[0]

    return render(request, 'actor.twig', {
        'actor': act,
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