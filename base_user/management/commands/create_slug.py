from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()



class Command(BaseCommand):
    help = "This command automatically create sulg field all User models"

    def handle(self, *args, **options):
        print("Let's started ...")

        all_user = User.objects.all()
        for slug in all_user:
            slug.save()

        print("-- All User objects create slug completed")