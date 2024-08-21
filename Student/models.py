from django.db import models
from django.utils import timezone
import uuid

class Student(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    date_of_birth = models.DateField(null=False)
    admission_date = models.DateField(default=timezone.now)
    address = models.TextField(null=False)
    education = models.CharField(max_length=200, null=False)
    education_type = models.CharField(max_length=100,null=False )
    email = models.EmailField(max_length=50, blank=True, null=True)
    perents_name = models.CharField(max_length=100, blank=True, null=True)
    perents_contact = models.CharField(max_length=15, blank=True, null=True)
    enrollment_status = models.CharField(max_length=100,null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.name
