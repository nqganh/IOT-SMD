from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('user', 'sip_username', 'sip_password', 'imei')
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        super(DeviceForm, self).__init__(*args, **kwargs)
