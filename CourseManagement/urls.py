
from django.urls import path
from Authentication.views import *

from CourseManagement.views import *


urlpatterns = [    
    path('courses-admin/', CourseView.as_view(), name='courses-admin'),
    path('courses-admin/details/', CourseDetails.as_view(), name='admin-course-details'),
    path('courses-teachers/', MyCourses.as_view(), name='courses-teachers'),
    path('courses-teachers/details/', CoursesDetails.as_view(), name='teachers-course-details'),
    path('exames-teachers/', ExamsTeachers.as_view(), name='exames-teachers'),
    path('academic-calender/', academic_calendar_public_view, name="calender"),
    

    # Student 
    path('', CoursesStudents.as_view(), name='courses'), 
    path('my-courses-student/', StudentEnrolledCourse.as_view(), name='my-courses-student/') ,
    path('my-courses-student/<pk>/', EnroledCourseDetails.as_view(), name='enrolledcourse'),
    path('view-result/<pk>/', ViewResults.as_view(), name='result_view')
    
]
