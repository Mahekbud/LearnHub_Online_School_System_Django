from django.db import models
from django.utils import timezone
import uuid

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=100) 
    hire_date = models.DateField(default=timezone.now)  
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
  
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.subject})"
