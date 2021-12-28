from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from epanel.constants.account import UserRole


class Command(BaseCommand):

    def handle(self, *args, **options):
        self._create_user_roles()

    def _create_user_roles(self):
        try:
            counter = 0
            for key, value in UserRole.CHOICES:
                group = Group.objects.all().filter(name=value).first()
                counter += 1
                if not isinstance(group, Group):
                    Group.objects.create(name=value)
                else:
                    group.name = value
                    group.save()

            if Group.objects.all().count() == counter:
                self.stdout.write(self.style.SUCCESS("User role data have been initialized!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
