from django.db import models
from django.conf import settings
from donors.models import Donor
import uuid

class BloodRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Fulfilled', 'Fulfilled'),
        ('Cancelled', 'Cancelled'),
    )
    BLOOD_GROUPS = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blood_requests')
    patient_name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units_required = models.IntegerField(default=1)
    location_city = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    urgency = models.CharField(max_length=50, choices=[('Normal', 'Normal'), ('Urgent', 'Urgent'), ('Critical', 'Critical')], default='Normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    tracking_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group} request for {self.patient_name}"

class DonorResponse(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    )
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='responses')
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='request_responses')
    response_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor} -> {self.blood_request} ({self.status})"

class BedRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    BED_TYPES = (
        ('ICU', 'ICU'),
        ('Oxygen', 'Oxygen'),
        ('General', 'General'),
    )
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    patient_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True, null=True, help_text="Email for status updates")
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE, related_name='bed_requests')
    bed_type = models.CharField(max_length=20, choices=BED_TYPES)
    emergency_notes = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    tracking_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bed_type} bed request at {self.hospital.name} for {self.patient_name}"
