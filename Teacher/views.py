from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Teacher
from .serializers import TeacherSerializer


#------------------------create_teacher-------------------------

@api_view(['POST'])
def create_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------get_teacher_by_id-----------------------

@api_view(['GET'])
def get_teacher_by_id(request):
    teacher_id = request.query_params.get('teacher_id')
    
    if not teacher_id:
        return Response({"error": "Teacher ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        teacher = Teacher.objects.get(id=teacher_id, is_active=True, is_deleted=False)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TeacherSerializer(teacher)
    return Response(serializer.data, status=status.HTTP_200_OK)

#-----------------------get_all_teacher----------------------

@api_view(["GET"])
def get_all_teacher(request):
    users = Teacher.objects.all()
    serializer = TeacherSerializer(users, many=True)
    return Response(serializer.data)


#-------------------update_teacher-------------------

@api_view(['PUT'])
def update_teacher_by_id(request):
    teacher_id = request.query_params.get('teacher_id')
    
    if not teacher_id:
        return Response({"error": "Teacher ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        teacher = Teacher.objects.get(id=teacher_id, is_active=True, is_deleted=False)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TeacherSerializer(teacher, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#--------------------------delete_teacher---------------------------

@api_view(['DELETE'])
def delete_teacher_by_id(request):
    teacher_id = request.query_params.get('teacher_id')
    if not teacher_id:
        return Response({"error": "Teacher ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        teacher = Teacher.objects.get(id=teacher_id, is_active=True, is_deleted=False)
        teacher.is_deleted = True
        teacher.save()
        return Response({"message": "Teacher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
    
#-----------------------get_teachers_by_subject--------------------------

@api_view(['GET'])
def get_teachers_by_subject(request):
    subject = request.query_params.get('subject')
    
    if not subject:
        return Response({"error": "Subject parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    teachers = Teacher.objects.filter(subject__icontains=subject, is_active=True, is_deleted=False)
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)