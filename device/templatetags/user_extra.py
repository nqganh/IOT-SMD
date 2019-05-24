from django import template
from django.db.models import Sum,Count
from user.models import User
from device.models import Extension
from django.conf import settings
register = template.Library()


@register.filter
def get_client(ext):
    try:
        return User.objects.get(id=ext.accountcode.id)
    except:
        return ''
