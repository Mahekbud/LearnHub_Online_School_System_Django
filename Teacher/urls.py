from django.urls import path
from .views import create_teacher,get_teacher_by_id,get_all_teacher,update_teacher_by_id,delete_teacher_by_id,get_teachers_by_subject

urlpatterns = [
    path('create_teacher/', create_teacher, name='create_teacher'),
    path('get_teacher_by_id/',get_teacher_by_id,name='get_teacher_by_id'),
    path('get_all_teacher/',get_all_teacher,name='get_all_teacher'),
    path('update_teacher_by_id/',update_teacher_by_id,name='update_teacher_by_id'),
    path('delete_teacher_by_id/',delete_teacher_by_id,name='delete_teacher_by_id'),
    path('get_teachers_by_subject/',get_teachers_by_subject,name='get_teachers_by_subject'),
]
