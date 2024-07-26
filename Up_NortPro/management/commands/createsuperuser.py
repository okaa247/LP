from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import CommandError

class Command(BaseCommand):
    help = 'Create a superuser with additional fields'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        fullname = input("Enter full name: ")
        phone_number = input("Enter phone number: ")

        if User.objects.filter(username=username).exists():
            raise CommandError('A user with this username already exists.')

        if User.objects.filter(email=email).exists():
            raise CommandError('A user with this email already exists.')

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            fullname=fullname,
            phone_number=phone_number
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created superuser with username {username}'))
