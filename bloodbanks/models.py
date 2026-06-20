from django.db import models
from django.conf import settings

class BloodBank(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bloodbank_profile')
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)
    
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Blood stock in units/bags
    a_pos = models.IntegerField(default=0, verbose_name="A+")
    a_neg = models.IntegerField(default=0, verbose_name="A-")
    b_pos = models.IntegerField(default=0, verbose_name="B+")
    b_neg = models.IntegerField(default=0, verbose_name="B-")
    ab_pos = models.IntegerField(default=0, verbose_name="AB+")
    ab_neg = models.IntegerField(default=0, verbose_name="AB-")
    o_pos = models.IntegerField(default=0, verbose_name="O+")
    o_neg = models.IntegerField(default=0, verbose_name="O-")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
