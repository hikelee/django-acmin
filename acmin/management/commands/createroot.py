from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from acmin.models import Group, User, GroupPermission, SuperPermissionModel, Model
        group = Group.objects.update_or_create(name="root")[0]

        user = User.objects.filter(username="root").first()
        if not user:
            user = User(group=group, username="root", title="root")
            user.set_password("123456")
            user.save()
        model = Model.objects.filter(name=SuperPermissionModel.__name__).first()

        permission = GroupPermission.objects.filter(group=group, model=model).first()
        if not permission:
            GroupPermission.objects.create(
                group=group,
                model=model,
                name="root",
                creatable=True,
                savable=True,
                removable=True,
                cloneable=True,
                exportable=True,
                viewable=True,
                listable=True,
            )
