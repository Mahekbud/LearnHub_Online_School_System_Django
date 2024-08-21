from django.urls import path
from .views import create_classroom,get_classroom_by_id,get_all_classroom,update_classroom_by_id,delete_classroom,search_students_by_education

urlpatterns = [
    path('create_classroom/', create_classroom, name='create-classroom'),
    path('get_classroom_by_id/',get_classroom_by_id,name='get_classroom_by_id'),
    path('get_all_classroom/', get_all_classroom, name='get_all_classroom'),
    path('update_classroom_by_id/', update_classroom_by_id, name='update-classroom-by-id'),
    path('delete_classroom/',delete_classroom,name='delete_classroom'),
    path('search_students_by_education/',search_students_by_education,name='search_students_by_education')
    
]