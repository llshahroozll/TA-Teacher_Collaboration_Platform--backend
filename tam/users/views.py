from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from courses.serializers import CourseTitleSerializer
# Create your views here.


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getProfiles(request):
#     profiles = Profile.objects.all()
#     serializer = ProfileSerializer(profiles, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    profile = request.user.profile
    profileSerializer = ProfileSerializer(profile, many=False)
    
    if profile.teacher_tag : 
        teacherCourses = profile.course_set.all()
        teacherCoursesSerializer = CourseTitleSerializer(teacherCourses, many=True)
        
        return Response({"profile": profileSerializer.data,
                        "teacherCourses": teacherCoursesSerializer.data,
                        })
        
    else:
        studentCourses = profile.studentCourses.all()
        assistantCourses = profile.assistantCourses.all()
        
        studentCourseSerializer = CourseTitleSerializer(studentCourses, many=True)
        assistantCoursesSerializer = CourseTitleSerializer(assistantCourses, many=True)
        
        
        return Response({"profile": profileSerializer.data,
                        "studentCourses": studentCourseSerializer.data,
                        "taCourses": assistantCoursesSerializer.data,
                        })
