from django.db import models
from django.utils import timezone
import uuid

class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=30)
    teacher = models.ForeignKey('Teacher.Teacher', on_delete=models.CASCADE, related_name='classrooms')
    students = models.ManyToManyField('Student.Student', related_name='classrooms', blank=True)
    education = models.CharField(max_length=10) 
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name