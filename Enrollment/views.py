

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Enrollment
from .serializers import EnrollmentSerializer



#-------------------------create_Enrollment----------------------------

@api_view(['POST'])
def create_enrollment(request):
    serializer = EnrollmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#----------------------------get_enrollment_by_id-----------------------------


@api_view(['GET'])
def get_enrollment_by_id(request):
    enrollment_id = request.query_params.get('id')
    if not enrollment_id:
        return Response({"error": "ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        return Response({"error": "Enrollment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EnrollmentSerializer(enrollment)
    return Response(serializer.data, status=status.HTTP_200_OK)


#------------------------get_all_enrollments----------------------------

@api_view(['GET'])
def get_all_enrollments(request):
    enrollments = Enrollment.objects.all()
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#---------------------------update_enrollments-------------------------

@api_view(['PUT'])
def update_enrollment_by_id(request):
    enrollment_id = request.query_params.get('id')
    
    if not enrollment_id:
        return Response({"error": "ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        return Response({"error": "Enrollment not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = EnrollmentSerializer(enrollment, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#-----------------------------delete_enrollment--------------------------

@api_view(['DELETE'])
def delete_enrollment_by_id(request):
    enrollment_id = request.query_params.get('id')
    
    if not enrollment_id:
        return Response({"error": "ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
        enrollment.delete()
        return Response({"message": "Enrollment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Enrollment.DoesNotExist:
        return Response({"error": "Enrollment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
#--------------------------get_enrollments_by_student-------------------------

@api_view(['GET'])
def get_enrollments_by_student(request):
    student_id = request.query_params.get('student_id')
    
    if not student_id:
        return Response({"error": "Student ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        enrollments = Enrollment.objects.filter(student_id=student_id)
        if not enrollments.exists():
            return Response({"error": "No enrollments found for this student."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#-----------------------------get_enrollments_by_course------------------------------------


@api_view(['GET'])
def get_enrollments_by_course(request):
    course_id = request.query_params.get('course_id')
    
    if not course_id:
        return Response({"error": "Course ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        enrollments = Enrollment.objects.filter(course_id=course_id)
        if not enrollments.exists():
            return Response({"error": "No enrollments found for this course."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#----------------------------get_enrollments_by_status-------------------------------

@api_view(['GET'])
def get_enrollments_by_status(request):
    status_param = request.query_params.get('status')
    
    if not status_param:
        return Response({"error": "Status parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        enrollments = Enrollment.objects.filter(status=status_param)
        if not enrollments.exists():
            return Response({"error": "No enrollments found with the specified status."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#------------------------------get_enrollments_by_date_range----------------------------------

@api_view(['GET'])
def get_enrollments_by_date_range(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if not start_date or not end_date:
        return Response({"error": "Both start_date and end_date parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        enrollments = Enrollment.objects.filter(enrollment_date__range=[start_date, end_date])
        if not enrollments.exists():
            return Response({"error": "No enrollments found in the specified date range."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)