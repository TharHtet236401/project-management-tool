from django.core.management.base import BaseCommand
from base.models import Project
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Creates dummy projects for testing'

    def handle(self, *args, **kwargs):
        # Project names and descriptions
        project_names = [
            "Website Redesign", "Mobile App Development", "Database Migration",
            "Cloud Infrastructure", "E-commerce Platform", "Content Management System",
            "Customer Portal", "Analytics Dashboard", "API Integration",
            "Security Audit", "Performance Optimization", "UI/UX Enhancement",
            "Payment Gateway", "Inventory System", "CRM Implementation",
            "Marketing Automation", "Data Analytics", "Machine Learning Model",
            "IoT Integration", "Blockchain Development"
        ]

        descriptions = [
            "A comprehensive project to improve user experience and modernize the interface.",
            "Developing a cross-platform mobile application with advanced features.",
            "Migrating legacy database systems to modern cloud-based solutions.",
            "Setting up and configuring cloud infrastructure for better scalability.",
            "Building a robust e-commerce platform with payment integration.",
            "Implementing a custom content management system for better content control.",
            "Creating a customer portal for self-service and support.",
            "Developing an analytics dashboard for business intelligence.",
            "Integrating third-party APIs for enhanced functionality.",
            "Conducting a thorough security audit and implementing improvements.",
            "Optimizing system performance for better user experience.",
            "Enhancing user interface and experience based on feedback.",
            "Implementing secure payment processing solutions.",
            "Developing an inventory management system with real-time tracking.",
            "Implementing a customer relationship management system.",
            "Setting up automated marketing workflows and campaigns.",
            "Building data analytics tools for business insights.",
            "Developing and training machine learning models for predictions.",
            "Integrating IoT devices for smart functionality.",
            "Building blockchain-based solutions for secure transactions."
        ]

        statuses = ['Not Started', 'In Progress', 'Completed']

        # Create 50 dummy projects
        for i in range(50):
            start_date = datetime.now() - timedelta(days=random.randint(0, 30))
            end_date = start_date + timedelta(days=random.randint(30, 90))
            
            project = Project.objects.create(
                name=f"{random.choice(project_names)} {i+1}",
                description=random.choice(descriptions),
                start_date=start_date,
                end_date=end_date,
                status=random.choice(statuses)
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created project: {project.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully created 50 dummy projects')) 