from django.db import models
import uuid
from django.utils import timezone




class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    u_name = models.CharField(max_length=20, null=False,unique=True)
    email = models.EmailField(max_length=50, null=False,unique=True)
    phone_no = models.CharField(max_length=15, null=False)
    password = models.CharField(max_length=100, null=False)
    date_of_birth = models.DateField(null=False)
    gender = models.CharField(max_length=10, null=False)
    address = models.TextField(null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.u_name
    
#---------------otp------------------

from django.db import models
from django.utils import timezone
import uuid

class Otp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100) 
    otp = models.CharField(max_length=50)
    expiration_time = models.DateTimeField(default=timezone.now) 

    def is_expired(self):
        return timezone.now() > self.expiration_time

    def __str__(self):
        return f'OTP {self.otp} for {self.email}'