import json

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Novel, Matcher, Tag

from pprint import pprint

def index(request):
    novels = Novel.objects.order_by('-id').all()

    return render(request, 'list.twig', {
        'novels': novels,
    })


def novel(request, id):
    novel = Novel.objects.get(id=id)
    matchers = Matcher.objects.filter(novel=novel)

    # construct body of the novel from txt files uploaded
    file_lines = novel.file.readlines()
    file_lines_decoded = []
    # including line numbers
    for n, line in enumerate(file_lines):
        line_decoded = None
        try:
            line_decoded = line.decode("utf-8")
        except:
            line_decoded = line.decode("gb18030")
        file_lines_decoded.append({'n':n, 'text': line_decoded}) 

    # tags
    tags = Tag.objects.order_by('weight').all()

    # match the actors to novel characters
    images = []
    for matcher in matchers:
        # replace actors
        for i, line in enumerate(file_lines_decoded):
            file_lines_decoded[i]['text'] = line['text'].replace(matcher.match, f'{matcher.prefix or ""}{matcher.actor.name}')
        # construct actor image sets
        images += matcher.actor.images.all()

    # tags->images
    tags_image_urls = []
    for idx, tag in enumerate(tags):
        image_urls = []
        for image in images:
            if tag in image.tags.all():
                image_urls.append(image.file.url)
        tags_image_urls.append({
            'tag': tag.name,
            'idx': idx,
            'image_urls': image_urls,
        })

    return render(request, 'novel.twig', {
        'novel': novel,
        'content': file_lines_decoded,
        'images': json.dumps(tags_image_urls),
        'tags': tags_image_urls,
    })