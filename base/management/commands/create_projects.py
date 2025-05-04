from django.core.management.base import BaseCommand
from base.models import Project, Profile
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Creates dummy projects and assigns users to them'

    def handle(self, *args, **kwargs):
        try:
            # Get all profiles
            managers = Profile.objects.filter(role='manager')
            developers = Profile.objects.filter(role='developer')
            designers = Profile.objects.filter(role='designer')

            # Project names and descriptions
            project_names = [
                "E-commerce Platform", "Mobile Banking App", "Social Media Dashboard",
                "Inventory Management", "Customer Support Portal", "Learning Management System",
                "Healthcare Management", "Event Planning Platform", "Real Estate Portal",
                "Fitness Tracking App", "Food Delivery Service", "Travel Booking System",
                "Document Management", "HR Management System", "Project Management Tool",
                "Online Learning Platform", "Fleet Management", "Hotel Booking System",
                "E-learning Platform", "Content Management System", "CRM System",
                "Task Management App", "Survey Platform", "Job Board",
                "Blog Platform", "Forum System", "Video Streaming Service",
                "Music Streaming App", "Weather App", "News Aggregator",
                "Recipe Sharing Platform", "Fitness Challenge App", "Language Learning App",
                "Budget Tracking App", "Home Automation System", "Car Rental Service",
                "Pet Care Platform", "Gaming Platform", "Virtual Classroom",
                "Online Marketplace", "Subscription Management", "Payment Gateway",
                "Analytics Dashboard", "Email Marketing Tool", "Social Network",
                "Video Conferencing", "File Sharing Platform", "Online Store",
                "Booking System", "Membership Portal"
            ]

            project_descriptions = [
                "A comprehensive platform for online shopping and payment processing",
                "Secure mobile application for banking and financial transactions",
                "Dashboard for managing social media accounts and analytics",
                "System for tracking and managing inventory across multiple locations",
                "Portal for handling customer support tickets and queries",
                "Platform for managing online courses and student progress",
                "System for managing patient records and healthcare services",
                "Platform for organizing and managing events and attendees",
                "Portal for property listings and real estate transactions",
                "Application for tracking fitness goals and progress",
                "Service for ordering and delivering food from local restaurants",
                "System for booking flights, hotels, and travel packages",
                "Platform for storing and managing digital documents",
                "System for managing employee records and HR processes",
                "Tool for managing projects, tasks, and team collaboration",
                "Platform for online courses and educational content",
                "System for managing vehicle fleets and logistics",
                "Platform for booking hotel rooms and accommodations",
                "System for delivering online educational content",
                "Platform for managing website content and publishing",
                "System for managing customer relationships and sales",
                "Application for managing tasks and to-do lists",
                "Platform for creating and conducting online surveys",
                "Website for posting and finding job opportunities",
                "Platform for publishing and managing blog content",
                "System for online discussions and community building",
                "Service for streaming video content online",
                "Application for streaming music and playlists",
                "App for tracking weather conditions and forecasts",
                "Platform for aggregating news from various sources",
                "Website for sharing and discovering recipes",
                "App for tracking fitness challenges and progress",
                "Platform for learning new languages online",
                "Application for tracking personal finances",
                "System for controlling smart home devices",
                "Service for renting cars and vehicles",
                "Platform for pet care services and products",
                "System for online gaming and tournaments",
                "Platform for virtual classrooms and learning",
                "Website for buying and selling products",
                "System for managing subscription services",
                "Platform for processing online payments",
                "Dashboard for analyzing business data",
                "Tool for managing email marketing campaigns",
                "Platform for social networking and sharing",
                "System for online video meetings and calls",
                "Platform for sharing and storing files",
                "Website for selling products online",
                "System for booking appointments and services",
                "Portal for managing membership programs"
            ]

            # Create 50 projects
            for i in range(50):
                # Random project details
                name = random.choice(project_names)
                description = random.choice(project_descriptions)
                status = random.choice(['pending', 'in_progress', 'completed'])
                
                # Random dates within the last year
                start_date = datetime.now() - timedelta(days=random.randint(0, 365))
                end_date = start_date + timedelta(days=random.randint(30, 365))

                # Create project
                project = Project.objects.create(
                    name=name,
                    description=description,
                    status=status,
                    start_date=start_date,
                    end_date=end_date
                )

                # Assign team members
                # Each project gets 1 manager, 2-4 developers, and 1-3 designers
                project.members.add(random.choice(managers))
                
                # Add 2-4 developers
                num_developers = random.randint(2, 4)
                project.members.add(*random.sample(list(developers), min(num_developers, len(developers))))
                
                # Add 1-3 designers
                num_designers = random.randint(1, 3)
                project.members.add(*random.sample(list(designers), min(num_designers, len(designers))))

                self.stdout.write(self.style.SUCCESS(f'Successfully created project: {name}'))

            self.stdout.write(self.style.SUCCESS('Successfully created all projects with assigned team members'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating projects: {str(e)}')) 