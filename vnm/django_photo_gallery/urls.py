from django.urls import path

from django.conf.urls import url
from django.contrib.auth import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

import app.forms
import app.views

from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', app.views.actors, name='actors'),
    path('image/<int:image_id>', app.views.image, name='image'),
    path('actor/<str:name>', app.views.actor, name='actor'),
    path('rnd/<int:actor_id>', app.views.rnd, name='rnd'),
    path('story/<int:story_id>', app.views.story, name='story'),
    path('viewer/<int:image_id>', app.views.viewer, name='viewer'),
    path('imageframe/<int:image_id>', app.views.imageframe, name='imageframe'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),
    #url(r'^(?P<slug>[-\w]+)$', app.views.ActorDetail.as_view(), name='image'), 
     
    # Auth related urls
    
    url(r'^accounts/login/$', views.LoginView, name='login'),
    url(r'^logout$', views.LogoutView, { 'next_page': '/', }, name='logout'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'app.views.handler404'




