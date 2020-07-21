from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Novel, Matcher

from pprint import pprint

def index(request):
    novels = Novel.objects.all()

    return render(request, 'list.twig', {
        'novels': novels,
    })

def novel(request, id):
    novel = Novel.objects.get(id=id)
    matchers = Matcher.objects.filter(novel=novel)

    file_lines = novel.file.readlines()
    file_lines_decoded = []
    for n, line in enumerate(file_lines):
        line_decoded = None
        try:
            line_decoded = line.decode("utf-8")
        except:
            line_decoded = line.decode("gb18030")
        file_lines_decoded.append({'n':n, 'text': line_decoded}) 

    for matcher in matchers:

        for i, line in enumerate(file_lines_decoded):
            file_lines_decoded[i]['text'] = line['text'].replace(matcher.match, f'{matcher.prefix or ""}{matcher.actor.name}')

    return render(request, 'novel.twig', {
        'novel': novel,
        'content': file_lines_decoded,
    })