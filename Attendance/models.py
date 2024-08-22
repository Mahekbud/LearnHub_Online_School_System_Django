from django.db import models
from django.utils import timezone
import uuid



class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey('Student.Student', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course.Course', on_delete=models.CASCADE)
    classroom_id = models.ForeignKey('Classroom.Classroom', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, default='Present')
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student_id.name} - {self.course_id.title} - {self.date} - {self.status}'

    
  
   
#  STATUS_CHOICES = [
#         ('Present', 'Present'),
#         ('Absent', 'Absent'),
#         ('Late', 'Late'),
#     ]