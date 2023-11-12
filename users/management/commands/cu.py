from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
                email='test@gmail.com',
                first_name='User',
                last_name='User',
                phone='12345678',
                is_active=True,
            )

        user.set_password('test')
        user.save()
