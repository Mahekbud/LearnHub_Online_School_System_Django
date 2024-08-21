from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer
from .models import Student
from django.utils.dateparse import parse_date


#----------------------------create_student-----------------------------

@api_view(['POST'])
def create_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#----------------------get_student_by_id------------------------


@api_view(['GET'])
def get_student_by_id(request):
    student_id = request.query_params.get('student_id')
    if not student_id:
        return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    print(f"Student ID: {student_id}")
    try:
        student = Student.objects.get(id=student_id, is_active=True, is_deleted=False)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)

#--------------------------get_all_student----------------------------

@api_view(["GET"])
def get_all_student(request):
    users = Student.objects.all()
    serializer = StudentSerializer(users, many=True)
    return Response(serializer.data)


#---------------------------update_student-------------------------

@api_view(['PUT'])
def update_student(request):
    student_id = request.query_params.get('student_id')
    if not student_id:
        return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=student_id, is_active=True, is_deleted=False)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-------------------------delete_student---------------------

@api_view(['DELETE'])
def delete_student(request):
    student_id = request.query_params.get('student_id')
    if not student_id:
        return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=student_id, is_active=True, is_deleted=False)
        student.is_deleted = True
        student.save()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

#------------------------get_students_by_education----------------------

@api_view(['GET'])
def get_students_by_education(request):
    education_level = request.query_params.get('education', None)

    if not education_level:
        return Response({"error": "Education level is required"}, status=status.HTTP_400_BAD_REQUEST)

    students = Student.objects.filter(education=education_level, is_active=True, is_deleted=False)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#----------------------------get_students_by_admission_date-----------------------------

@api_view(['GET'])
def get_students_by_admission_date(request):
    admission_date = request.query_params.get('admission_date')
    
    if not admission_date:
        return Response({"error": "Admission date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    students = Student.objects.filter(admission_date=admission_date, is_active=True, is_deleted=False)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#------------------------------get_students_list_by_admission_date---------------------------
@api_view(['GET'])
def get_students_list_by_admission_date(request):
    admission_date_str = request.query_params.get('admission_date')
    
    if not admission_date_str:
        return Response({"error": "Admission date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    admission_date = parse_date(admission_date_str)
    
    if not admission_date:
        return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    
    students = Student.objects.filter(admission_date__gte=admission_date, is_active=True, is_deleted=False)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)