from django.urls import path
from .views import create_student,get_student_by_id,get_all_student,update_student,delete_student,get_students_by_education,get_students_by_admission_date
from .views import get_students_list_by_admission_date


urlpatterns = [
    path('create_student/', create_student, name='create_student'),
    path('get_student_by_id/', get_student_by_id, name='get_student_by_id'),
    path('get_all_student/',get_all_student,name='get_all_student'),
    path('update_student/', update_student, name='update_student'),
    path('delete_student/',delete_student,name='delete_student'),
    path('get_students_by_education/',get_students_by_education,name='get_students_by_education'),
    path('get_students_by_admission_date/',get_students_by_admission_date,name='get_students_by_admission_date'),
    path('get_students_list_by_admission_date/',get_students_list_by_admission_date,name='get_students_list_by_admission_date'),
]


