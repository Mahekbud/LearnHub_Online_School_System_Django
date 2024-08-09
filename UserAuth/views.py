from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from datetime import timedelta
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from .models import User, Otp
from django.core.exceptions import ValidationError
import bcrypt
import random
import uuid
import json
from jose import JWTError
from .utils import get_token,decode_token_user_id
from django.conf import settings



#----------------------- create user --------------------------

@api_view(["POST"])
def create_user(request):
    data = request.data
    data["password"] = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#----------------------------generet otp--------------------------

    
@api_view(["POST"])
def generate_otp(request):
    email = request.data.get("email")
    
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

    otp_value = ''.join(str(random.randint(0, 9)) for _ in range(6))
    expiration_time = timezone.now() + timedelta(minutes=10)
    otp_id = str(uuid.uuid4())
    
    otp_record = Otp(
        id=otp_id,
        email=email,
        otp=otp_value,
        expiration_time=expiration_time
    )
    otp_record.save()

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp_value}, which is valid for 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )

    return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


#------------------------------verify otp-------------------------


@api_view(["POST"])
def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        entered_otp = data.get('otp')
        
        if not email or not entered_otp:
            return JsonResponse({"error": "Email and OTP are required"}, status=400)

        try:
            stored_otp = Otp.objects.filter(email=email).first()
            
            if stored_otp:
                if timezone.now() < stored_otp.expiration_time:
                    if entered_otp == stored_otp.otp:
                        stored_otp.delete()

                        user = User.objects.filter(email=email, is_active=True, is_deleted=False).first()
                        if user:
                            user.is_verified = True
                            user.save()
                            return Response({"message": "OTP verification successful"})

                        else:
                            return JsonResponse({"error": "User not found"}, status=404)
                    else:
                        return JsonResponse({"error": "Incorrect OTP entered"}, status=400)
                else:
                    stored_otp.delete()
                    return JsonResponse({"error": "OTP has expired"}, status=400)
            else:
                return JsonResponse({"error": "No OTP record found for the user"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

#-------------------------------login-----------------------

@api_view(["POST"])
def login(request):
    uname = request.data.get("uname")
    password = request.data.get("password")

    if not uname or not password:
        return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(u_name=uname)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=uname)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Debugging info
    print(f"Original password provided: {password}")
    print(f"Stored password hash: {user.password}")

    # Check password
    password_matches = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
    print(f"Password match result: {password_matches}")

    if password_matches:
        if not user.is_verified:
            return Response({"message": "User not verified"}, status=status.HTTP_403_FORBIDDEN)

        token = get_token(user.id)
        return Response({"token": token}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


    
#------------------------------get_user_by_token--------------------------------

@api_view(['GET'])
def get_user_by_token(request):

    token = request.headers.get('Authorization')
    if not token:
        return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = decode_token_user_id(token)
    if not user_id:
        return Response({"error": "Invalid token or user ID extraction failed"}, status=status.HTTP_400_BAD_REQUEST)

    db_user = User.objects.filter(id=user_id, is_active=True, is_verified=True, is_deleted=False).first()
    if db_user is None:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(db_user)
    serialized_data = serializer.data
    return Response(serialized_data)

#------------------------------get_all_token----------------------------

@api_view(["GET"])
def get_all_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

#---------------------------update_user_by_token-----------------------

@api_view(['PUT'])
def update_user_by_token(request):
    token = request.headers.get('Authorization')
    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user_id_from_token = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = User.objects.get(pk=user_id_from_token) 
    except (User.DoesNotExist, ValidationError):
        return Response({'error': 'User not found or invalid user ID'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#----------------------- delete_user_by_token----------------------


@api_view(['DELETE'])
def delete_user_by_token(request):
    token = request.headers.get('Authorization')
    
    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        user_id_from_token = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        user_to_delete = User.objects.get(pk=user_id_from_token)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user_id_from_token != str(user_to_delete.id):
        return Response({'error': 'Unauthorized to delete this user'}, status=status.HTTP_403_FORBIDDEN)
    
    user_to_delete.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#--------------------------forget password------------------------------------

@api_view(['PUT'])
def forget_password(request):
    token = request.headers.get('Authorization')
    new_password = request.data.get('user_newpass')

    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

    if not new_password:
        return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        db_user = User.objects.get(id=user_id, is_active=True, is_verified=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not db_user.is_verified:
        return Response({'error': 'User not verified'}, status=status.HTTP_403_FORBIDDEN)

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db_user.password = hashed_password
    db_user.save()
    
    return Response({'message': 'Password forget successfully'}, status=status.HTTP_200_OK)

#-----------------------------reset password-----------------------------

@api_view(['PUT'])
def reset_password_by_token(request):
    token = request.headers.get('Authorization')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

    if not old_password or not new_password:
        return Response({'error': 'Old and new passwords are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        db_user = User.objects.get(id=user_id, is_active=True, is_verified=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the old password matches
    if not bcrypt.checkpw(old_password.encode('utf-8'), db_user.password.encode('utf-8')):
        return Response({'error': 'Old password does not match'}, status=status.HTTP_400_BAD_REQUEST)

    # Set new password
    db_user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user.save()

    return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

