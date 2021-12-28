from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from epanel.constants.account import UserRole
from epanel.constants.admin import AdminPermission


class Command(BaseCommand):

    def handle(self, *args, **options):
        self._create_group_permission()

    def _create_group_permission(self):
        try:
            groups = Group.objects.all()
            is_user_permission = Permission.objects.all().filter(codename=AdminPermission.CODE_NAME_IS_USER).first()
            is_admin_permission = Permission.objects.all().filter(codename=AdminPermission.CODE_NAME_IS_ADMIN).first()
            user_group = groups.filter(name=UserRole.USER_NAME).first()
            if is_user_permission not in user_group.permissions.all():
                user_group.permissions.add(is_user_permission)

            admin_groups = groups.filter(name__in=UserRole.NAME_LIST[:2])
            for admin_group in admin_groups:
                if is_admin_permission not in admin_group.permissions.all():
                    admin_group.permissions.add(is_admin_permission)
            self.stdout.write(self.style.SUCCESS("User group permission data have been initialized!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))

