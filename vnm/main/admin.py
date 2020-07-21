from django.contrib import admin

from .models import Novel, Actor, Matcher

class MatcherInline(admin.StackedInline):
    model = Matcher
    # max_num=maximun number of editable objects inline, extra=additional object that doesn't exceed max_num
    extra = 0

class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')

    inlines = [
        MatcherInline,
    ]

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', )

# Register your models here.
admin.site.register(Novel, NovelAdmin)
admin.site.register(Actor, ActorAdmin)