from django import forms
from user.models import User
from .models import Extension

class ExtensionForm(forms.ModelForm):
    client = forms.ModelChoiceField(required=False, queryset=User.objects.exclude(role=1))
    class Meta:
        model = Extension
        fields = ('client', 'extension_uuid')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        super(ExtensionForm, self).__init__(*args, **kwargs)
