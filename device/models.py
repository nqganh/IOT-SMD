from django.utils.translation import get_language_from_request, ugettext_lazy as _
from django.db import models

# Create your models here.
from user.models import User

class Device(models.Model):
    user = models.ForeignKey(User)
    sip_username = models.CharField(max_length=16)
    sip_password = models.CharField(max_length=64)
    imei = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.sip_username
