from django.urls import path
from .views import create_exam,get_exam_by_id,get_all_exams,update_exam_by_id,delete_exam_by_id,get_exams_by_course,get_exams_by_type
from .views import get_exams_by_student ,get_upcoming_exams


urlpatterns = [
    path('create_exam/', create_exam, name='create_exam'),
    path('get_exam_by_id/',get_exam_by_id,name='get_exam_by_id'),
    path('get_all_exams/',get_all_exams,name='get_all_exams'),
    path('update_exam_by_id/',update_exam_by_id,name='update_exam_by_id'),
    path('delete_exam_by_id/',delete_exam_by_id,name='delete_exam_by_id'),
    path('get_exams_by_course/' ,get_exams_by_course,name='get_exams_by_course' ),
    path('get_exams_by_type/',get_exams_by_type,name='get_exams_by_type'),
    path('get_exams_by_student/',get_exams_by_student,name='get_exams_by_student'),
    path('get_upcoming_exams/',get_upcoming_exams,name='get_upcoming_exams')
 
]