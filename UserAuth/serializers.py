from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'




    # class Meta:
    #     model = User
    #     fields = [
    #         'id', 'role', 'email', 'u_name', 'password', 'date_of_birth',
    #         'phone_no', 'address', 'gender', 'is_active', 'is_deleted',
    #         'is_verified', 'create_at', 'modified_at'
    #     ]