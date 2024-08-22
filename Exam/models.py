
from django.db import models
from django.utils import timezone
import uuid


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
        ('midterm', 'Midterm'),
        ('final', 'Final'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey('Student.Student', on_delete=models.CASCADE, related_name='exams')
    course_id = models.ForeignKey('Course.Course', on_delete=models.CASCADE, related_name='exams')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    exam_date = models.DateField()
    duration = models.DurationField()  
    total_marks = models.IntegerField()  
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.get_exam_type_display()} Exam for {self.student.name} in {self.course.name} on {self.exam_date}'

