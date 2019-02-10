from django.contrib import admin
from device.models import Extension, RingGroup, RingGroupDestination, DialPlan
# Register your models here.
admin.site.register(Extension)
admin.site.register(RingGroup)
admin.site.register(RingGroupDestination)
admin.site.register(DialPlan)
