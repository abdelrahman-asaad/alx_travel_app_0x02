from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        # Create some sample users if they don't exist
        users = User.objects.all()
        if not users:
            for i in range(1, 4):
                User.objects.create_user(username=f"user{i}", password="pass1234")
            users = User.objects.all()

        # Sample listings
        sample_titles = ["Beach House", "Mountain Cabin", "City Apartment"]
        for title in sample_titles:
            Listing.objects.create(
                title=title,
                description=f"A wonderful place called {title}",
                price=random.randint(50, 500),
                owner=random.choice(users)
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
