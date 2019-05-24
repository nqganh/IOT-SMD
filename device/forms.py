from django import forms
from user.models import User, RingGroup
from .models import Extension, RingGroupDestination

class ExtensionForm(forms.ModelForm):
    client = forms.ModelChoiceField(required=False, queryset=User.objects.exclude(role=1))
    class Meta:
        model = Extension
        fields = ('client', 'extension_uuid')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        super(ExtensionForm, self).__init__(*args, **kwargs)

class ExtensioniEditForm(forms.ModelForm):
    client = forms.ModelChoiceField(required=False, queryset=User.objects.exclude(role=1))
    class Meta:
        model = Extension
        fields = ('client', 'extension_uuid', 'do_not_disturb', 'description')
        widgets = {
            'do_not_disturb': forms.Select(choices=(('',''),('true','true'),('false','false'))),
            'description': forms.Select(choices=(('',''),('is_bell','is_bell'))),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        super(ExtensioniEditForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = "Sip's a bell"

class DepartmentForm(forms.ModelForm):
    client = forms.ModelChoiceField(required=False, queryset=User.objects.exclude(role=1))
    class Meta:
        model = RingGroup
        fields = ('client', 'ring_group_uuid', 'ring_group_name')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        super(DepartmentForm, self).__init__(*args, **kwargs)

class DepartmentDTForm(forms.ModelForm):
#    client = forms.ModelChoiceField(required=False, queryset=User.objects.filter(email='nguyenquocuong13@gmail.com'))
    client = forms.CharField(required=False)
    class Meta:
        model = RingGroup
        fields = ('client', 'ring_group_uuid', 'ring_group_name', 'ring_group_extension')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        self.email = kwargs.pop('email', None)
        super(DepartmentDTForm, self).__init__(*args, **kwargs)

class DepartmentOptionForm(forms.ModelForm):
    client = forms.ModelChoiceField(required=False, queryset=User.objects.exclude(role=1))
#    client = forms.ModelChoiceField(required=False)
    class Meta:
        model = RingGroupDestination
        fields = ('client', 'ring_group_uuid', 'destination_number')

    def clean_ring_group_uuid(self, *args, **kwargs):
        rg_uu = self.cleaned_data.get('ring_group_uuid')
        client = self.cleaned_data.get('client')
        client_rr = User.objects.filter(email=client)
        for abc in client_rr:
            kk = abc.ring_group.all()
            if rg_uu not in kk:
                raise forms.ValidationError("This department is not in user's list")
            else:
                return rg_uu

    def clean_destination_number(self, *args, **kwargs):
        des_num = self.cleaned_data.get('destination_number')
        client = self.cleaned_data.get('client')
        client_id = User.objects.get(email=client)
        liex = Extension.objects.filter(accountcode=client_id)
        if des_num not in liex:
            raise forms.ValidationError("Sip account is not in user's list")
        else:
            if RingGroupDestination.objects.filter(destination_number=des_num).count() == 0:
                if Extension.objects.get(extension=des_num).description == 'is_bell':
                    raise forms.ValidationError("Sip account is bell")
                else:
                    return des_num
            else:
                raise forms.ValidationError("Sip account exists in this department")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        super(DepartmentOptionForm, self).__init__(*args, **kwargs)

class RGDCreateForm(forms.ModelForm):
    client = forms.ModelChoiceField(required=False, queryset=User.objects.exclude(role=1))
    class Meta:
        model = RingGroupDestination
        fields = ('client', 'ring_group_uuid', 'destination_number')

    def clean_client(self, *args, **kwargs):
        client = self.cleaned_data.get('client')
        if client == "" or client == None:
            raise forms.ValidationError("Please select a department")
        else:
            return client

    def clean_ring_group_uuid(self, *args, **kwargs):
        rg_uu = self.cleaned_data.get('ring_group_uuid')
        if rg_uu == "" or rg_uu == None:
            raise forms.ValidationError("Please select a department")
        else:
            return rg_uu
    def clean_destination_number(self, *args, **kwargs):
        des_num = self.cleaned_data.get('destination_number')
        if des_num == "" or des_num == None:
            raise forms.ValidationError("Please select a sip account")
        else:
            return des_num

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.role = kwargs.pop('role', None)
        self.email = kwargs.pop('email', None)
        super(RGDCreateForm, self).__init__(*args, **kwargs)
        self.fields['destination_number'].queryset = Extension.objects.none()
        self.fields['ring_group_uuid'].queryset = RingGroup.objects.none()
        if 'client' in self.data:
            try:
                client_id = self.data.get('client')
                client_obj = User.objects.filter(id=client_id)
                for obj in client_obj:
                    self.fields['ring_group_uuid'].queryset = obj.ring_group.all().order_by('ring_group_name')
                if 'ring_group_uuid' in self.data:
                    try:
                         rg_uuid = self.data.get('ring_group_uuid')
                         lisiex = RingGroupDestination.objects.filter(ring_group_uuid=rg_uuid)
                         if len(lisiex) != 0:
                             test = lisiex.values_list('destination_number', flat=True)
                             self.fields['destination_number'].queryset = Extension.objects.filter(accountcode=client_id).exclude(description="is_bell").exclude(extension__in=test)
                         else:
                             self.fields['destination_number'].queryset = Extension.objects.filter(accountcode=client_id).exclude(description="is_bell")
                    except (ValueError, TypeError):
                        pass
            except (ValueError, TypeError):
                pass
