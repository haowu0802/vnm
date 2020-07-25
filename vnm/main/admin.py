from django.contrib import admin

from .models import Novel, Actor, Matcher, Image, Tag

class TagListFilter(admin.SimpleListFilter):
    
    title = 'Has tag'

    parameter_name = 'has_tag'

    def lookups(self, request, model_admin):

        return (
            ('yes', 'Yes'),
            ('no',  'No'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter(tags__isnull=False)

        if self.value() == 'no':
            return queryset.filter(tags__isnull=True)

class MatcherInline(admin.StackedInline):
    model = Matcher
    # max_num=maximun number of editable objects inline, extra=additional object that doesn't exceed max_num
    extra = 0

class NovelAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'file')

    inlines = [
        MatcherInline,
    ]

    def get_title(self, obj):
        return obj.title or obj.file.name

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'actor', 'get_tags', 'file')
    readonly_fields = ['image_tag']

    list_filter = [TagListFilter,]


    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'


# Register your models here.
admin.site.register(Novel, NovelAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag)