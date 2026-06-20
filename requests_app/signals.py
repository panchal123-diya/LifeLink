from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import BloodRequest, BedRequest
from donors.models import Donor

@receiver(post_save, sender=BloodRequest)
def notify_donors_on_blood_request(sender, instance, created, **kwargs):
    if created:
        # Find eligible donors in the same city with matching blood group
        # Note: A real app would also consider blood group compatibility, but for simplicity we match exactly.
        eligible_donors = Donor.objects.filter(
            blood_group=instance.blood_group,
            is_available=True,
            # In a real app we'd filter by city too, but Donor model doesn't currently store city!
            # Let's just notify matching blood group for now.
        )
        
        recipient_list = [donor.user.email for donor in eligible_donors if donor.user.email and donor.is_eligible]
        
        if recipient_list:
            subject = f"URGENT: {instance.blood_group} Blood Required for {instance.patient_name}"
            message = (
                f"Hello Donor,\n\n"
                f"An urgent blood request has been posted for {instance.blood_group} blood.\n"
                f"Patient: {instance.patient_name}\n"
                f"Hospital: {instance.hospital_name}, {instance.location_city}\n"
                f"Units Required: {instance.units_required}\n"
                f"Urgency: {instance.urgency}\n\n"
                f"Please log in to HealthBridge to respond to this request."
            )
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@healthbridge.com',
                recipient_list,
                fail_silently=True,
            )

@receiver(post_save, sender=BedRequest)
def notify_patient_on_bed_request_update(sender, instance, created, **kwargs):
    if not created and instance.contact_email:
        if instance.status in ['Approved', 'Rejected']:
            subject = f"Update: Your Bed Request at {instance.hospital.name} is {instance.status}"
            message = (
                f"Hello {instance.patient_name},\n\n"
                f"Your request for a {instance.bed_type} bed at {instance.hospital.name} has been {instance.status.upper()}.\n\n"
            )
            
            if instance.status == 'Approved':
                message += "Please contact the hospital immediately or proceed to the admission desk.\n"
                message += f"Hospital Contact: {instance.hospital.phone}\n\n"
            else:
                message += "We are sorry, but the hospital could not accommodate your request at this time. Please try requesting at another nearby hospital.\n\n"
                
            message += f"You can track your request here: http://127.0.0.1:8000/requests/track-bed/{instance.tracking_token}/\n"
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@healthbridge.com',
                [instance.contact_email],
                fail_silently=True,
            )
