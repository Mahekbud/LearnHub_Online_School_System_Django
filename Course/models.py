from django.db import models
from django.utils import timezone
import uuid




class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_name = models.CharField(max_length=100)  # Name of the course
    description = models.TextField()  # Description of the course
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.name})"

#   EDUCATION_LEVEL_CHOICES = [
#         ('Jr. KG', 'Jr. KG'),
#         ('Sr. KG', 'Sr. KG'),
#         ('Primary', 'Primary Education (Grades 1-5)'),
#         ('Middle', 'Middle School (Grades 6-8)'),
        #   ('Grade_9', 'Grade 9'),
        #   ('Grade_10', 'Grade 10'),
        # ('Grade_11_Science', 'Grade 11 Science Stream'),
        # ('Grade_11_Commerce', 'Grade 11 Commerce Stream'),
        # ('Grade_11_Arts', 'Grade 11 Arts Stream'),
        # ('Grade_12_Science', 'Grade 12 Science Stream'),
        # ('Grade_12_Commerce', 'Grade 12 Commerce Stream'),
        # ('Grade_12_Arts', 'Grade 12 Arts Stream'),
#     