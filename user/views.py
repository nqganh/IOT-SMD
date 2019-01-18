from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView, CreateView, YearArchiveView, TemplateView, UpdateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import get_current_site
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from .forms import LoginForm, UserCreationForm, UserChangeForm
from .models import User, ADMIN, CUSTOMER


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

    # Allow filter 
    def get_queryset_filters(self):
        filters = {}
        try:
            for item in self.allowed_filters:
                if item in self.request.GET and self.request.GET[item]:
                     filters[self.allowed_filters[item]] = self.request.GET[item]
            return filters
        except AttributeError:
            return filters

    def get_queryset(self):
        return super(LoginRequiredMixin, self).get_queryset()\
              .filter(**self.get_queryset_filters())


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"


class LoginView(FormView):
    """
    Displays the login form and handles the login action.
    """
    form_class = LoginForm
    template_name = 'user/login.html'
    extra_context = None
    success_url = '/'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            "site": current_site,
            "site_name": current_site.name,
        })
        context.update(self.extra_context or {})
        return context

class AccountList(LoginRequiredMixin, ListView):
    model = User
    paginate_by = settings.PAGINATE_BY
    allowed_filters = {
        'user': 'sure_name',
    }

    def get_paginate_by(self, queryset):
        if self.request.GET.get('paginate_by'):
            return self.request.GET.get('paginate_by')
        return self.paginate_by

    def get_template_names(self):
        return ['user/account_list.html']

    def get_queryset(self):
        return super(AccountList, self).get_queryset().exclude(pk=self.request.user.id).filter(role=CUSTOMER).order_by('email')

    def get_context_data(self, **kwargs):
        context = super(AccountList, self).get_context_data(**kwargs)
        return context


class AccountAdd(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('account_list')
    template_name = 'add.html'

    def form_valid(self, form):
        form.instance.parent = self.request.user
        form.instance.role = CUSTOMER
        form.instance.is_active = True
        return super(AccountAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AccountAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['role'] = CUSTOMER
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AccountAdd, self).get_context_data(**kwargs)
        return context


class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'add.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('account_list')

    def form_valid(self, form):
        #self.object.picture = form.cleaned_data['picture']
        if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
            self.object.set_password(form.cleaned_data['password1'])
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(AccountUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AccountUpdate, self).get_context_data(**kwargs)
        return context


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('account_list')
    template_name = 'remove.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDelete, self).get_context_data(**kwargs)
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'add.html'
    form_class = UserChangeForm
    success_url = '/'

    def form_valid(self, form):
        #self.object.picture = form.cleaned_data['picture']
        if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
            self.object.set_password(form.cleaned_data['password1'])
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)
