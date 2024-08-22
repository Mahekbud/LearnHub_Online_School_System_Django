from django.urls import path
from .views import create_attendance,get_attendance_by_id,get_all_attendances,update_attendance_by_id,delete_attendance_by_id
from .views import search_attendance_by_status,get_attendance_by_classroom_id,get_attendance_by_student_id,get_attendance_by_course_id


urlpatterns = [
    path('create_attendance/', create_attendance, name='create_attendance'),
    path('get_attendance_by_id/',get_attendance_by_id,name='get_attendance_by_id'),
    path('get_all_attendances/',get_all_attendances,name='get_all_attendances'),
    path('update_attendance_by_id/',update_attendance_by_id,name='update_attendance_by_id'),
    path('delete_attendance_by_id/',delete_attendance_by_id,name='delete_attendance_by_id'),
    path('search_attendance_by_status/',search_attendance_by_status,name='search_attendance_by_status'),
    path('get_attendance_by_classroom_id/',get_attendance_by_classroom_id,name='get_attendance_by_classroom_id'),
    path('get_attendance_by_student_id/',get_attendance_by_student_id,name='get_attendance_by_student_id'),
    path('get_attendance_by_course_id/',get_attendance_by_course_id,name='get_attendance_by_course_id')
   

]