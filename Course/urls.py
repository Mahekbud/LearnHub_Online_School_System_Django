from django.urls import path
from .views import create_course,get_course_by_id,get_all_courses,update_course,delete_course



urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('get_course_by_id/', get_course_by_id, name='get-course-by-id'),
    path('get_all_courses/', get_all_courses, name='get-all-courses'),
    path('update_course/',update_course,name='update_course'),
    path('delete_course/',delete_course,name='delete_course'),

]