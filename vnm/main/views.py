from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Novel

def index(request):
    # Load documents for the list page
    novels = Novel.objects.all()

    return render(request, 'list.twig', {
        'novels': novels,
    })