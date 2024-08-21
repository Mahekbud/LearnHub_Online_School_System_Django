from django.db import models
from django.utils import timezone
import uuid

class Enrollment(models.Model):
             
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey('Student.Student', on_delete=models.CASCADE)  # Reference to Student model in Student app
    course_id = models.ForeignKey('Course.Course', on_delete=models.CASCADE) 
    enrollment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20,default='Active')
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student_id} - {self.course_id} ({self.status})"

