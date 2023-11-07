from django.conf import settings
from django import template
register = template.Library()
from main.models import *

@register.simple_tag
def get_header():
    software_list = Software.objects.all()

    

    context = {
        'software_list': software_list,
    }
    return context