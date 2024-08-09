from django.urls import path
from .views import create_user,generate_otp,verify_otp,login,get_user_by_token,get_all_user,update_user_by_token,delete_user_by_token,forget_password,reset_password_by_token

urlpatterns = [
    path('get_all_user/', get_all_user, name='get_all_user'),  
    path('create-user/', create_user, name='create-user'),   
    path('generate-otp/', generate_otp, name='generate_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', login, name='login'), 
    path('get_user_by_token/', get_user_by_token, name='get_user_by_token'), 
    path('delete_user_by_token/',delete_user_by_token,name = 'delete_user_by_token'),
    path('update_user_by_token/',update_user_by_token,name='update_user_by_token'),
    path('forget_password/',forget_password,name='forget_password'),
    path('reset_password_by_token/',reset_password_by_token,name='reset_password_by_token'),
    
]