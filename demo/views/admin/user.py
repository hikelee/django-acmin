from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from acmin.utils import attr
from demo.forms.user import LoginForm, UserForm
from acmin.models import User
from . import BaseCreateView, BaseListView, BaseUpdateView


class UserListView(BaseListView):
    model = User


class FormMixin:
    model = User

    def form_valid(self, form):
        user = form.save(False)
        password = form.cleaned_data['password1']
        if password and len(password) > 0:
            user.set_password(password)
            user.save()
        return super().form_valid(form)

    def get_form_class(self):
        return UserForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class UserCreateView(FormMixin, BaseCreateView):
    pass


class UserUpdateView(FormMixin, BaseUpdateView):
    pass


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = '/'
    redirect_field_name = REDIRECT_FIELD_NAME

    def get(self, request, *args, **kwargs):
        self.request = request
        logout(request)
        return super().get(request, *args, **kwargs)

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = attr(settings, 'INDEX_URL')
        kwargs['redirect_to'] = redirect_to

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            # redirect_to = self.request.GET.get(self.redirect_field_name)
            auth.login(self.request, form.get_user())
            return super().form_valid(form)
            # return HttpResponseRedirect('/')
        else:
            return self.render_to_response({'form': form})

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=[self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to
