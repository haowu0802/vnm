#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from os import listdir
from os.path import isfile, join

from django.conf import settings

from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

from app.models import Actor, ActorImage

def gallery(request):
    list = Actor.objects.all().order_by('-created')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        actors = paginator.page(page)
    except PageNotAnInteger:
        actors = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        actors = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'gallery.html', { 'actors': list })


def actors(request):
    """this view loads data from local hd
    """
    actor_list = [f for f in listdir(settings.LOCAL_PATH) if not isfile(join(settings.LOCAL_PATH, f))]
    return render(request, 'actors.twig', { 'actors': actor_list })


def actor(request, name):
    print(name)
    images = []
    return render(request, 'actor.twig', {
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