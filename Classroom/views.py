from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Classroom
from .serializers import ClassroomSerializer
from Student.models import Student



#--------------------------create_classroom------------------------

@api_view(['POST'])
def create_classroom(request):
    serializer = ClassroomSerializer(data=request.data)
    if serializer.is_valid():
        classroom = serializer.save()
        classroom_education = classroom.education
        
        # Retrieve students with the same education level
        students = Student.objects.filter(education=classroom_education)
        
        # Assign these students to the classroom
        if students.exists():
            classroom.students.set(students)
            classroom.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#------------------------get_classroom_by_id-----------------------

@api_view(['GET'])
def get_classroom_by_id(request):
    classroom_id = request.query_params.get('id')
    if not classroom_id:
        return Response({"error": "Classroom ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        classroom = Classroom.objects.get(id=classroom_id)
    except Classroom.DoesNotExist:
        return Response({"error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassroomSerializer(classroom)
    return Response(serializer.data, status=status.HTTP_200_OK)

#------------------------------get_all_classroom----------------------------

@api_view(['GET'])
def get_all_classroom(request):
    classrooms = Classroom.objects.all()
    serializer = ClassroomSerializer(classrooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#-----------------------update_classroom_by_id----------------------------


@api_view(['PUT'])
def update_classroom_by_id(request):
    classroom_id = request.query_params.get('id')
    if not classroom_id:
        return Response({"error": "Classroom ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        classroom = Classroom.objects.get(id=classroom_id)
    except Classroom.DoesNotExist:
        return Response({"error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassroomSerializer(classroom, data=request.data, partial=True)
    
    if serializer.is_valid():
        updated_classroom = serializer.save()
        new_education = updated_classroom.education
        
        # Retrieve students with the same education level
        students = Student.objects.filter(education=new_education)
        
        # Assign these students to the classroom
        if students.exists():
            updated_classroom.students.set(students)
            updated_classroom.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#----------------------------delete_classroom_by_id--------------------------

@api_view(['DELETE'])
def delete_classroom(request):
    classroom_id = request.query_params.get('id')
    if not classroom_id:
        return Response({"error": "Classroom ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        classroom = Classroom.objects.get(id=classroom_id)
    except Classroom.DoesNotExist:
        return Response({"error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)
    
    classroom.is_deleted = True
    classroom.save()

    return Response({"message": "Classroom deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

#--------------------------------------------------------------

@api_view(['GET'])
def search_students_by_education(request):
    education_level = request.query_params.get('education', None)
    
    if not education_level:
        return Response({"error": "Education level is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    students = Student.objects.filter(education=education_level)
    
    if not students.exists():
        return Response({"message": "No students found for the given education level."}, status=status.HTTP_404_NOT_FOUND)
    
    student_data = [
        {
            "id": student.id,
            "name": student.name,
            "date_of_birth": student.date_of_birth,
            "address": student.address,
            "education": student.education,
            "education_type": student.education_type,
            "email": student.email,
            "perents_name": student.perents_name,
            "perents_contact": student.perents_contact,
            "enrollment_status": student.enrollment_status,
            "grade": student.grade,
            "percentage": student.percentage
        }
        for student in students
    ]
    
    return Response({"students": student_data, "count": students.count()}, status=status.HTTP_200_OK)

