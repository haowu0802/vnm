from django.contrib import admin

from .models import Novel

class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')

# Register your models here.
admin.site.register(Novel, NovelAdmin)