from django.contrib import admin
from CourseManagement.models import *


# Register your models here.
admin.site.register(Subjects)
admin.site.register(Chapters)
admin.site.register(Lessons)
admin.site.register(Exams)
admin.site.register(Questions)
admin.site.register(CourseEnrollApplication)
admin.site.register(StudentAnswer)
