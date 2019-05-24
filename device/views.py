import random, string
import uuid
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView, CreateView, YearArchiveView, TemplateView, UpdateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import get_current_site
from user.views import LoginRequiredMixin
from django.conf import settings
from user.models import CUSTOMER, ADMIN, User
from .models import Extension, RingGroup, RingGroupDestination
from .forms import  ExtensionForm, DepartmentForm, DepartmentDTForm, DepartmentOptionForm, RGDCreateForm, ExtensioniEditForm

# Create your views here.
class DeviceList(LoginRequiredMixin, ListView):
    model = Extension
    template_name = 'device/device_list.html'
    paginate_by = settings.PAGINATE_BY
    allowed_filters = {
        'user': 'sure_name',
    }
    def get_paginate_by(self, queryset):
        if self.request.GET.get('paginate_by'):
            return self.request.GET.get('paginate_by')
        return self.paginate_by
    
    def get_queryset(self):
        return super(DeviceList, self).get_queryset().order_by('accountcode')

    

    def get_context_data(self, **kwargs):
        context = super(DeviceList, self).get_context_data(**kwargs)
        return context


class DeviceAdd(LoginRequiredMixin, CreateView):
    model = Extension
    form_class = ExtensionForm
    success_url = reverse_lazy('device_list')
    template_name = 'device/device_update.html'
    
    def form_valid(self, form):
        form.instance.accountcode = form.cleaned_data['client']
        i = 0
        while i < 10000000:
            i += 1
            form.instance.extension = random.randint(1000000,9999999)
            if Extension.objects.filter(extension=form.instance.extension).count() == 0:
                break
        form.instance.extension = random.randint(1000000,9999999)
        form.instance.password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
        return super(DeviceAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(DeviceAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DeviceAdd, self).get_context_data(**kwargs)
        return context


class DeviceUpdate(LoginRequiredMixin, UpdateView):
    model = Extension
    template_name = 'device/device_update.html'
    form_class = ExtensioniEditForm
    success_url = reverse_lazy('device_list')

    def get_initial(self):
        if self.object.accountcode:
            client = self.object.accountcode
            return {'client': client}
        return {}

    def form_valid(self, form):
        self.object.accountcode = form.cleaned_data['client']
        if form.cleaned_data['do_not_disturb'] == 'true':
            self.object.do_not_disturb = form.cleaned_data['do_not_disturb']
            self.object.dial_string = 'error/user_busy'
        else:
            self.object.do_not_disturb = ''
            self.object.dial_string = ''
        
        self.object.description = form.cleaned_data['description']
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(DeviceUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DeviceUpdate, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return Extension.objects.get(extension_uuid=self.kwargs['uuid'])


class DeviceDelete(LoginRequiredMixin, DeleteView):
    model = Extension
    success_url = reverse_lazy('device_list')
    template_name = 'remove.html'

    def get_object(self, queryset=None):
        return Extension.objects.get(extension_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(DeviceDelete, self).get_context_data(**kwargs)
        return context


class RGList(LoginRequiredMixin, ListView):
    model = RingGroup
    template_name = 'device/rg_list.html'

    def get_paginate_by(self, queryset):
        if self.request.GET.get('paginate_by'):
            return self.request.GET.get('paginate_by')
        return self.paginate_by

    def get_queryset(self):
        pk = self.request.user.ring_group.all()
        if self.request.user.role == 1:
            return super(RGList, self).get_queryset().order_by('ring_group_name')
        else:
            if self.request.user.role == 2:
                return super(RGList, self).get_queryset().filter(ring_group_uuid__in=pk).order_by('ring_group_name')
#                return super(RGList, self).get_queryset().order_by('ring_group_name')

    def get_context_data(self, **kwargs):
        context = super(RGList, self).get_context_data(**kwargs)
        return context

class RGAdd(LoginRequiredMixin, CreateView):
    model = RingGroup
    form_class = DepartmentForm
    success_url = reverse_lazy('department_list')
    template_name = 'aedep.html'
    
    def form_valid(self, form):
        rg = RingGroup()
        form.instance.ring_group_extension = random.randint(100000,999999)
#        rg.ring_group_extension = random.randint(100000,999999)
        form.instance.ring_group_name = form.cleaned_data['ring_group_name']
        form.instance.ring_group_uuid = form.cleaned_data['ring_group_uuid']
        form.instance.save()
        User.objects.get(email=form.cleaned_data['client']).ring_group.add(form.cleaned_data['ring_group_uuid'])
        return super(RGAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(RGAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RGAdd, self).get_context_data(**kwargs)
        return context


class RGUpdate(LoginRequiredMixin, UpdateView):
    model = RingGroup
    template_name = 'aedep.html'
    form_class = DepartmentDTForm
    success_url = reverse_lazy('department_list')
    def get_initial(self):
        lrg = self.object.user.all()
        if self.object.user:
            client = lrg[0]
            return {'client': client}
        return {}

    def get_form_kwargs(self):
        kwargs = super(RGUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RGUpdate, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return RingGroup.objects.get(ring_group_uuid=self.kwargs['uuid'])

class RGDelete(LoginRequiredMixin, DeleteView):
    model = RingGroup
    success_url = reverse_lazy('department_list')
    template_name = 'remove.html'

    def get_object(self, queryset=None):
        return RingGroup.objects.get(ring_group_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(RGDelete, self).get_context_data(**kwargs)
        return context

class RGDList(LoginRequiredMixin, ListView):
    model = RingGroupDestination
    template_name = 'device/rgd_list.html'

    def get_paginate_by(self, queryset):
        if self.request.GET.get('paginate_by'):
            return self.request.GET.get('paginate_by')
        return self.paginate_by

    def get_queryset(self):
        pk = self.request.user.ring_group.all()
        if self.request.user.role == 1:
            return super(RGDList, self).get_queryset().order_by('destination_number')
        else:
            if self.request.user.role == 2:
                return super(RGDList, self).get_queryset().filter(ring_group_uuid__in=pk).order_by('destination_number')
#        return super(RGDList, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(RGDList, self).get_context_data(**kwargs)
        return context

class RGDCreate(LoginRequiredMixin, CreateView):
    model = RingGroupDestination
    form_class = RGDCreateForm
    success_url = reverse_lazy('rgd_list')
    template_name = 'device/aedecreate.html'
    
    def get_form_kwargs(self):
        kwargs = super(RGDCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.ring_group_destination_uuid = uuid.uuid4()
        form.instance.ring_group_uuid = form.cleaned_data['ring_group_uuid']
        form.instance.destination_number = form.cleaned_data['destination_number']
        form.instance.save()
        return super(RGDCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(RGDCreate, self).get_context_data(**kwargs)
        return context


def load_rguuid(request):
    client_id = request.GET.get('client')
    if client_id != '':
        lirg = User.objects.get(pk=client_id).ring_group.all()
    else:
        lirg = []
    return render(request, 'device/rg_dropdown_list_options.html', {'ring_group_uuid': lirg})

def load_destinationnumber(request):
    client_id = request.GET.get('client')
    rg_uuid = request.GET.get('rguuid')
    lisiex = RingGroupDestination.objects.filter(ring_group_uuid=rg_uuid)
    if len(lisiex) != 0:
        test = lisiex.values_list('destination_number', flat=True)
        liex = Extension.objects.filter(accountcode=client_id).exclude(description="is_bell").exclude(extension__in=test)
    else:
        liex = Extension.objects.filter(accountcode=client_id).exclude(description="is_bell")
    return render(request, 'device/ex_dropdown_list_options.html', {'destination_number': liex})



class RGDAdd(LoginRequiredMixin, CreateView):
    model = RingGroupDestination
    form_class = DepartmentOptionForm
    success_url = reverse_lazy('rgd_list')
    template_name = 'aedea.html'
    
    def form_valid(self, form):
        form.instance.ring_group_destination_uuid = uuid.uuid4()
        form.instance.ring_group_uuid = form.cleaned_data['ring_group_uuid']
        form.instance.destination_number = form.cleaned_data['destination_number']
        form.instance.save()
        return super(RGDAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(RGDAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RGDAdd, self).get_context_data(**kwargs)
        return context 

class RGDUpdate(LoginRequiredMixin, UpdateView):
    model = RingGroupDestination
    template_name = 'aedea.html'
    form_class = DepartmentOptionForm
#    form_class = RGDCreateForm
    success_url = reverse_lazy('rgd_list')

    def get_initial(self):
        a = RingGroupDestination.objects.filter(ring_group_destination_uuid=self.kwargs['uuid'])
        for b in a:
            c = b.destination_number
            d = Extension.objects.filter(extension=c)
            for e in d:
                client = e.accountcode
                return {'client': client}
        return {}

    def get_form_kwargs(self):
        kwargs = super(RGDUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RGDUpdate, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return RingGroupDestination.objects.get(ring_group_destination_uuid=self.kwargs['uuid'])


class RGDDelete(LoginRequiredMixin, DeleteView):
    model = RingGroupDestination
    success_url = reverse_lazy('rgd_list')
    template_name = 'remove.html'

    def get_object(self, queryset=None):
        return RingGroupDestination.objects.get(ring_group_destination_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(RGDDelete, self).get_context_data(**kwargs)
        return context
