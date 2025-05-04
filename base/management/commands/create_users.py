from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base.models import Profile
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Creates users with balanced roles (3:10:8 ratio of manager:developer:designer)'

    def handle(self, *args, **kwargs):
        try:
            # Define the number of users for each role
            role_counts = {
                'manager': 3,
                'developer': 10,
                'designer': 8
            }

            # List of first names and last names for random generation
            first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Lisa', 
                         'William', 'Jennifer', 'James', 'Jessica', 'Thomas', 'Amanda', 'Daniel', 
                         'Melissa', 'Matthew', 'Stephanie', 'Christopher', 'Nicole', 'Andrew']
            
            last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                         'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 
                         'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

            # Create users for each role
            for role, count in role_counts.items():
                for i in range(count):
                    # Generate random user details
                    first_name = random.choice(first_names)
                    last_name = random.choice(last_names)
                    username = f"{first_name.lower()}.{last_name.lower()}{i+1}"
                    email = f"{username}@example.com"
                    password = "testpass123"  # Default password for all users

                    # Create user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )

                    # Create profile
                    Profile.objects.create(
                        user=user,
                        role=role,
                        phone=f"+1{random.randint(1000000000, 9999999999)}"  # Random US phone number
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully created {role}: {username}'))

            self.stdout.write(self.style.SUCCESS('Successfully created all users with balanced roles'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating users: {str(e)}')) 