#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from os import listdir
from os.path import isfile, join, getmtime, basename, exists
from pathlib import Path

from PIL import Image

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files import File
from django.core.files.images import ImageFile
from django.db.models.functions import Lower
from django.http import HttpRequest, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt


from app.models import Actor, ActorImage, ActorImageLocal, Story

from next_prev import next_in_order, prev_in_order


def create_image(story, filepath, actor=None, cate=None):
    if not ActorImageLocal.objects.filter(filepath=filepath).exists():
        ext = Path(filepath).suffix
        # video file skip dimentions
        if ext in ['.mp4']:
            width, height = 0, 0
        else:
            # get image dim
            im = Image.open(filepath)
            width, height = im.size
        # instantiate
        photo = ActorImageLocal(
            filepath=filepath,
            story=story,
            actor=actor,
            cate=cate,
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
    return render(request, 'stories.twig', { 
        'stories': story_list,
        'actor': act,
    })


# random pic viewer
def rnd(request, actor_id):
    # get actor
    actor = get_object_or_404(Actor, pk=actor_id)
    # ingest local files
    dir_path = join(settings.LOCAL_PATH, actor.name)
    # get cates
    cate_list = [f for f in listdir(dir_path) if not isfile(join(dir_path, f))]
    cate_list.sort()
    cate_list_opt = []
    # create images in cates
    for cate in cate_list:
        if not '_' in cate:
            cate_list_opt.append(cate)
            cate_dir = join(dir_path, cate)
            file_list = [f for f in listdir(cate_dir) if isfile(join(cate_dir, f))]
            for filename in file_list:
                filepath = join(cate_dir, filename)
                create_image(None, filepath, actor, cate)

    # remove deleted images
    images = ActorImageLocal.objects.all()
    for image in images:
        if not exists(image.filepath):
            image.delete()

    # all images of actor
    images_actor = ActorImageLocal.objects.filter(actor=actor)

    # default
    image_left = images_actor.order_by('?')[0]
    image_right = None

    # get cate from param
    cate_left = request.GET.getlist('cl')
    if cate_left:
        image_left = images_actor.filter(cate__in=list(cate_left)).order_by('?')[0]
    cate_right = request.GET.getlist('cr')
    if cate_right:
        image_right = images_actor.filter(cate__in=list(cate_right)).order_by('?')[0]

    # locks
    rightlock = request.GET.getlist('rightlock')
    if rightlock:
        image_right = images_actor.get(pk=rightlock[0])

    # get auto flag
    auto = request.GET.get('auto')

    return render(request, 'rnd.twig', { 
        'actor': actor,
        'image_left': image_left,
        'image_right': image_right,
        'cate_list': cate_list_opt,
        'cl': cate_left,
        'cr': cate_right,
        'auto': auto,
        'rightlock': rightlock,
    })


def story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    # refresh story
    refresh = request.GET.get('refresh')
    if refresh:
        story.thumb = None
        story.save()
        ActorImageLocal.objects.filter(story=story).all().delete()

    # get local image path from settings and fetch file list
    dir_path = story.filepath
    if not exists(dir_path):
        story.delete()
        return redirect(reverse('actor', kwargs={'name': story.actor.name}))

    file_list = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    for filename in file_list:
        filepath = join(dir_path, filename)
        create_image(story, filepath, story.actor, story.name)

    # remove deleted images
    images = ActorImageLocal.objects.filter(story=story)
    for image in images:
        if not exists(image.filepath):
            image.delete()

    # get images without +
    images = ActorImageLocal.objects.filter(actor=story.actor).filter(cate=story.name).order_by(Lower('filepath'))
    #images = ActorImageLocal.objects.filter(story=story).exclude(filepath__contains="+").order_by(Lower('filepath'))

    # ordering
    sort = request.GET.get('sort')
    if sort:
        images = images.order_by(sort),
        images = images[0]

    story_list = Story.objects.filter(actor=story.actor).order_by('filepath')
    story_prev = prev_in_order(story, qs=story_list)
    story_next = next_in_order(story, qs=story_list)


    #return render(request, 'actor.twig', {
    return render(request, 'story.twig', {
        'story': story,
        'images': images,
        'prev': story_prev,
        'next': story_next,
    })


def viewer(request, image_id):
    image = get_object_or_404(ActorImageLocal, pk=image_id)
    image_name = Path(image.filepath).stem

    story = image.story

    # get images with default sort (filename)
    images = ActorImageLocal.objects.filter(story=story).order_by('filepath')
    # ordering
    sort = request.GET.get('sort')
    if sort:
        images = images.order_by(sort),
        images = images[0]
    # get prev and next image
    image_prev = prev_in_order(image, qs=images)
    image_next = next_in_order(image, qs=images)

    return render(request, 'viewer.twig', {
        'image': image,
        'story': story,
        'actor': story.actor,
        'prev': image_prev,
        'next': image_next,
    })

@xframe_options_exempt
def imageframe(request, image_id):
    image = get_object_or_404(ActorImageLocal, pk=image_id)
    return render(request, 'imageframe.twig', {
        'image': image,
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