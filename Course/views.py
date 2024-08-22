from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer



#--------------------------create_course---------------------------

@api_view(['POST'])
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-------------------------get_id_by_course----------------------

@api_view(['GET'])
def get_course_by_id(request):
    course_id = request.query_params.get('id')
    if not course_id:
        return Response({"error": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(id=course_id,is_active=True, is_deleted=False)
    except Course.DoesNotExist:
        return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)


#-----------------------get_all_course------------------------

@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()  
    serializer = CourseSerializer(courses, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)


#-----------------------update_course------------------------------

@api_view(['PUT'])
def update_course(request):
    course_id = request.query_params.get('id')
    if not course_id:
        return Response({"error": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(id=course_id,is_active=True, is_deleted=False)
    except Course.DoesNotExist:
        return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-------------------------delete_course_by_id----------------------

@api_view(['DELETE'])
def delete_course(request):
    course_id = request.query_params.get('id')
    if not course_id:
        return Response({"error": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(id=course_id)
        course.delete()
        return Response({"message": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Course.DoesNotExist:
        return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
