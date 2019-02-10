import random, string
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
from .models import Extension
from .forms import  ExtensionForm

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
        if self.request.user.role == 1:
            return super(DeviceList, self).get_queryset()
        return super(DeviceList, self).get_queryset().exclude(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DeviceList, self).get_context_data(**kwargs)
        return context


class DeviceAdd(LoginRequiredMixin, CreateView):
    model = Extension
    form_class = ExtensionForm
    success_url = reverse_lazy('device_list')
    template_name = 'add.html'

    def form_valid(self, form):
        form.instance.accountcode = form.cleaned_data['client'].id
        form.instance.extension = random.randint(100000,999999)
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
    template_name = 'add.html'
    form_class = ExtensionForm
    success_url = reverse_lazy('device_list')

    def get_initial(self):
        if self.object.accountcode:
            client = User.objects.get(id=self.object.accountcode)
            return {'client': client}
        return {}

    def form_valid(self, form):
        self.object.accountcode = form.cleaned_data['client'].id
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
