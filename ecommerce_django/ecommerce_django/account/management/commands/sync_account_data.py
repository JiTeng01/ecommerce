from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from account.models import User, Account
from epanel.constants.account import UserRole, Status, Gender


class Command(BaseCommand):

    def handle(self, *args, **options):
        self._create_superuser_account()

    def _create_superuser_account(self):
        user, account = None, None
        try:
            username, email, password = "superadmin", "admin@gmail.com", "123123"
            if isinstance(User.objects.get_one_by_username(username), User):
                self.stdout.write(self.style.ERROR("Account has been existed already!"))
                return False

            user = User.objects.create_superuser(username, email, password)
            if not isinstance(user, User):
                self.stdout.write(self.style.ERROR("User has not been created!"))
            else:
                group = Group.objects.all().filter(name=UserRole.ADMIN_NAME).first()
                user.groups.add(group)
                full_name, nric = "Ecommerce Superadmin", ""
                account = Account.objects.create(user=user, full_name=full_name, gender=Gender.MALE, phone_number="11111")
                if not isinstance(account, Account):
                    self.stdout.write(self.style.ERROR("Account has not been created!"))
                else:
                    self.stdout.write(self.style.SUCCESS("Account has been created!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
            if isinstance(user, User):
                user.delete()
