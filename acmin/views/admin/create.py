from django.urls import reverse
from django.views.generic.edit import CreateView

from acmin.models import BasePermission, PermissionItem
from .form import AdminFormView


class AdminCreateView(AdminFormView, CreateView):
    success_message = "创建成功!"

    def has_permission(self):
        return BasePermission.has_permission(self.request.user, self.model, PermissionItem.creatable)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_action"] = reverse(f'{self.model.__name__}-create')
        context["view_type"] = 'create'
        obj = self.model
        setattr(obj, "_request", self.request)
        context["object"] = obj

        return context
