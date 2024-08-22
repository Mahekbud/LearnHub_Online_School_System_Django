from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .serializers import AttendanceSerializer



#-------------------------------create_attendance------------------------------
   
@api_view(['POST'])
def create_attendance(request):
    serializer = AttendanceSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#---------------------------get_attendance_by_id----------------------------


@api_view(['GET'])
def get_attendance_by_id(request):
    id = request.query_params.get('id')
    
    if not id:
        return Response({"error": "ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        attendance = Attendance.objects.get(id=id)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AttendanceSerializer(attendance)
    return Response(serializer.data, status=status.HTTP_200_OK)

#-----------------------------get_all_attendances---------------------------------

@api_view(['GET'])
def get_all_attendances(request):
 
    attendances = Attendance.objects.all()

    serializer = AttendanceSerializer(attendances, many=True)
   
    return Response(serializer.data, status=status.HTTP_200_OK)

#------------------------------update_attendance_by_id------------------------------

@api_view(['PUT'])
def update_attendance_by_id(request):
    id = request.query_params.get('id')
    
    if not id:
        return Response({"error": "ID query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        attendance = Attendance.objects.get(id=id, is_active=True, is_deleted=False)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------delete_attendance_by_id--------------------------------

@api_view(['DELETE'])
def delete_attendance_by_id(request):
    id = request.query_params.get('id')

    if not id:
        return Response({"error": "ID query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        attendance = Attendance.objects.get(id=id, is_active=True)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found."}, status=status.HTTP_404_NOT_FOUND)

    attendance.is_active = False
    attendance.save()

    return Response({"message": "Attendance record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

#-------------------------------search_attendance_by_status------------------------------

@api_view(['GET'])
def search_attendance_by_status(request):
    status_filter = request.query_params.get('status')
    
    if not status_filter:
        return Response({"error": "Status query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        attendances = Attendance.objects.filter(status=status_filter,is_active=True, is_deleted=False)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        return Response({"error": "Invalid status format."}, status=status.HTTP_400_BAD_REQUEST)
    
    
#-----------------------------get_attendance_by_classroom_id-----------------------------------

@api_view(['GET'])
def get_attendance_by_classroom_id(request):
    classroom_id = request.query_params.get('classroom_id')

    if not classroom_id:
        return Response({"error": "Classroom ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        attendances = Attendance.objects.filter(classroom_id=classroom_id,is_active=True, is_deleted=False)
     
        if not attendances.exists():
            return Response({"error": "No attendance records found for the specified classroom."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#------------------------------get_attendance_by_student_id--------------------------------

@api_view(['GET'])
def get_attendance_by_student_id(request):
    student_id = request.query_params.get('student_id')

    if not student_id:
        return Response({"error": "Student ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        attendances = Attendance.objects.filter(student_id=student_id,is_active=True, is_deleted=False)
   
        if not attendances.exists():
            return Response({"error": "No attendance records found for the specified student."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#-----------------------------get_attendance_by_course_id-------------------------------

@api_view(['GET'])
def get_attendance_by_course_id(request):
    course_id = request.query_params.get('course_id')

    if not course_id:
        return Response({"error": "Course ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        attendances = Attendance.objects.filter(course_id=course_id)

        if not attendances.exists():
            return Response({"error": "No attendance records found for the given course ID."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#--------------------------------------------------------------------------------

