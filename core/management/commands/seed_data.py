import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from accounts.models import User
from hospitals.models import Hospital
from bloodbanks.models import BloodBank
from donors.models import Donor
from requests_app.models import BloodRequest

class Command(BaseCommand):
    help = 'Seeds the database with initial data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            admin.role = 'admin'
            admin.save()
            self.stdout.write('Created admin user.')
            
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        # 10 Hospitals
        for i in range(1, 11):
            username = f'hospital_{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=f'{username}@example.com', password='password123', role='hospital', city=random.choice(cities))
                Hospital.objects.create(
                    user=user,
                    name=f'General Hospital {i}',
                    registration_number=f'REG-H-{1000+i}',
                    is_verified=True,
                    icu_beds=random.randint(5, 50),
                    oxygen_beds=random.randint(10, 100),
                    general_beds=random.randint(50, 500)
                )
                
        self.stdout.write('Created 10 Hospitals.')
                
        # 3 Blood Banks
        for i in range(1, 4):
            username = f'bloodbank_{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=f'{username}@example.com', password='password123', role='bloodbank', city=random.choice(cities))
                BloodBank.objects.create(
                    user=user,
                    name=f'City Blood Center {i}',
                    license_number=f'LIC-BB-{2000+i}',
                    is_verified=True,
                    a_pos=random.randint(0, 50),
                    a_neg=random.randint(0, 10),
                    b_pos=random.randint(0, 40),
                    b_neg=random.randint(0, 10),
                    ab_pos=random.randint(0, 20),
                    ab_neg=random.randint(0, 5),
                    o_pos=random.randint(0, 100),
                    o_neg=random.randint(0, 20)
                )
        self.stdout.write('Created 3 Blood Banks.')
                
        # 30 Donors
        for i in range(1, 31):
            username = f'donor_{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, 
                    email=f'{username}@example.com', 
                    password='password123', 
                    role='donor', 
                    city=random.choice(cities),
                    first_name=f'John',
                    last_name=f'Doe {i}'
                )
                
                # Randomize eligibility
                days_ago = random.randint(10, 150)
                last_donation = timezone.now().date() - timedelta(days=days_ago)
                
                Donor.objects.create(
                    user=user,
                    blood_group=random.choice(blood_groups),
                    last_donation_date=last_donation,
                    is_available=True
                )
        self.stdout.write('Created 30 Donors.')
        
        # Requests
        if not BloodRequest.objects.exists():
            admin_user = User.objects.get(username='admin')
            for i in range(5):
                BloodRequest.objects.create(
                    requester=admin_user,
                    patient_name=f'Patient {i}',
                    blood_group=random.choice(blood_groups),
                    units_required=random.randint(1, 4),
                    location_city=random.choice(cities),
                    hospital_name=f'General Hospital {random.randint(1,10)}',
                    urgency=random.choice(['Normal', 'Urgent', 'Critical'])
                )
        self.stdout.write('Created sample Requests.')
                
        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))
