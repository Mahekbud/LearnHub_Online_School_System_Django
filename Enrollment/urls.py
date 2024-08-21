from django.urls import path
from .views import create_enrollment,get_enrollment_by_id,get_all_enrollments,update_enrollment_by_id,delete_enrollment_by_id,get_enrollments_by_student
from .views import get_enrollments_by_course,get_enrollments_by_status,get_enrollments_by_date_range


urlpatterns = [
    path('create_enrollment/', create_enrollment, name='create_enrollment'),
    path('get_enrollment_by_id/',get_enrollment_by_id,name='get_enrollment_by_id'),
    path('get_all_enrollments/',get_all_enrollments,name='get_all_enrollments'),
    path('update_enrollment/',update_enrollment_by_id,name='update_enrollment'),
    path('delete_enrollment_by_id/',delete_enrollment_by_id,name='delete_enrollment_by_id'),
    path('get_enrollments_by_student/',get_enrollments_by_student,name='get_enrollments_by_student'),
    path('get_enrollments_by_course/',get_enrollments_by_course,name='get_enrollments_by_course'),
    path('get_enrollments_by_status/',get_enrollments_by_status,name='get_enrollments_by_status'),
    path('get_enrollments_by_date_range/',get_enrollments_by_date_range,name='get_enrollments_by_date_range')
 
]