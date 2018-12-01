from django.urls import reverse
from django.views.generic.edit import UpdateView

from acmin.models import Permission, PermissionItem
from .form import AdminFormView


class AdminUpdateView(AdminFormView, UpdateView):
    success_message = "更新成功!"

    def is_clone(self):
        return self.request.GET.get("clone") is not None

    def get_template_names(self):
        name = "create.html" if self.is_clone() else "update.html"
        return [f"admin/{self.model.__name__}/{name}", f'base/{name}']

    def has_permission(self):
        return Permission.has_permission(self.request.user, self.model, PermissionItem.viewable)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = self.get_object().get_absolute_url()
        context["view_type"] = 'update'
        if self.is_clone():
            obj = context["object"]
            obj.id = ""
            context["form_action"] = reverse(f'{self.model.__name__}-create')
            context["is_clone"] = True

        setattr(context.get('object'), "_request", self.request)
        return context
