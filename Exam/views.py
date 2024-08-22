from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Exam
from .serializers import ExamSerializer
from Enrollment.models import Enrollment




#----------------------------create_exam-------------------------------


@api_view(['POST'])
def create_exam(request):
    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        course_id = request.data.get('course_id')
        student_id = request.data.get('student_id')  

        if course_id is None or student_id is None:
            return Response({'error': 'Course ID and Student ID must be provided.'}, status=status.HTTP_400_BAD_REQUEST)
     
        if not Enrollment.objects.filter(student_id=student_id, course_id=course_id).exists():
            return Response({'error': 'Student is not enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------get_exam_by_id------------------------------------

@api_view(['GET'])
def get_exam_by_id(request):
    exam_id = request.query_params.get('exam_id')
    
    if exam_id is None:
        return Response({'error': 'Exam ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        exam = Exam.objects.get(id=exam_id,is_active=True, is_deleted=False)
        serializer = ExamSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exam.DoesNotExist:
        return Response({'error': 'Exam not found.'}, status=status.HTTP_404_NOT_FOUND)
    
#----------------------get_all_exams-----------------------

@api_view(['GET'])
def get_all_exams(request):
    exams = Exam.objects.all()  
    serializer = ExamSerializer(exams, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

#-------------------------update_exam_by_id--------------------------


@api_view(['PUT'])
def update_exam_by_id(request):
    exam_id = request.query_params.get('id')  
    
    if not exam_id:
        return Response({'error': 'Exam ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({'error': 'Exam not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    student_id = request.data.get('student_id')
    course_id = request.data.get('course_id')
 
    if student_id and course_id:
        if not Enrollment.objects.filter(student_id=student_id, course_id=course_id).exists():
            return Response({'error': 'Student is not enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)
  
    serializer = ExamSerializer(exam, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------delete_exam_by_id--------------------------------

@api_view(['DELETE'])
def delete_exam_by_id(request):
    exam_id = request.query_params.get('id') 
    
    if not exam_id:
        return Response({'error': 'Exam ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({'error': 'Exam not found.'}, status=status.HTTP_404_NOT_FOUND)
   
    exam.delete()
    
    return Response({'message': 'Exam deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

#------------------------------get_exams_by_course-----------------------------------


@api_view(['GET'])
def get_exams_by_course(request):
    course_id = request.query_params.get('course_id')
    
    if not course_id:
        return Response({'error': 'Course ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        exams = Exam.objects.filter(course_id=course_id)
        if not exams.exists():
            return Response({'error': 'No exams found for the given course ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#-------------------------get_exams_by_type--------------------------

@api_view(['GET'])
def get_exams_by_type(request):
    exam_type = request.query_params.get('exam_type')
    
    if not exam_type:
        return Response({'error': 'Exam type is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        exams = Exam.objects.filter(exam_type=exam_type)
        if not exams.exists():
            return Response({'error': 'No exams found for the given exam type.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#---------------------get_exams_by_student-------------------------

@api_view(['GET'])
def get_exams_by_student(request):
    student_id = request.query_params.get('student_id')
    
    if not student_id:
        return Response({'error': 'Student ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        exams = Exam.objects.filter(student_id=student_id)
        
        if not exams.exists():
            return Response({'error': 'No exams found for the given student.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------get_upcoming_exams---------------------------------------

from django.utils import timezone

@api_view(['GET'])
def get_upcoming_exams(request):
    now = timezone.now()
    exams = Exam.objects.filter(exam_date__gte=now)
    serializer = ExamSerializer(exams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
