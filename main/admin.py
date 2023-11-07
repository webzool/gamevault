from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.forms import TextInput, Textarea

from main.utils import export_to_csv
# Register your models here.
from .models import *



admin.site.register(GamesPage)
admin.site.register(ContactPage)
admin.site.register(Software)
admin.site.register(AweberCredentials)
admin.site.register(AweberLog)
admin.site.register(Category)
admin.site.register(Tag)



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'height':'650px'})},
    }
    def get_form(self, request, obj=None, **kwargs):
        form = super(BlogAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['content'].widget.attrs['style'] = 'height: 600px;'
        form.base_fields['content'].widget.attrs['style'] = 'color: black;'
        form.base_fields['tag'].widget.attrs['style'] = 'height: 155px;'
        form.base_fields['category'].widget.attrs['style'] = 'height: 155px;'
        return form


@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'height':'650px'})},
    }
    def get_form(self, request, obj=None, **kwargs):
        form = super(AboutPageContentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['meta_description'].widget.attrs['style'] = 'height: 100px !imortant;'
        form.base_fields['content'].widget.attrs['style'] = 'background-color: black; !important'
        return form


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )
    actions = [export_to_csv]


admin.site.register(Author)
