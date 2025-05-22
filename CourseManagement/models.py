from django.db import models

from Authentication.models import CustomUser

# Create your models here.

class Subjects(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_description = models.TextField(null=True, blank=True)
    subject_image = models.ImageField(upload_to='subjects/', null=True, blank=True)
    course_enrole_fee = models.FloatField(null=True,blank=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(CustomUser, related_name='students')
    status = models.BooleanField(default=True)
    is_admin_aproved = models.BooleanField(default=False)
    senester_rank = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name


class Chapters(models.Model):
    chapter_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    number_of_lessons = models.IntegerField(default=0)
    chapter_plan = models.FileField(upload_to='chapter_plan/', null=True, blank=True)
    status = models.BooleanField(default=True)
    is_admin_aproved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chapter_name


class Lessons(models.Model):
    lesson_name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)

    assignment = models.FileField(upload_to='assignment/', null=True, blank=True)
    lsat_date_of_submission = models.DateField(null=True, blank=True)
    live_class_date = models.DateTimeField(null=True, blank=True)
    live_class_link = models.URLField(null=True, blank=True)
    resource_file = models.FileField(upload_to='resource_file/', null=True, blank=True)
    lesson_video = models.FileField(upload_to='lesson_video/', null=True, blank=True)
    iframe_data = models.TextField(null=True, blank=True)
    lesson_note = models.FileField(upload_to='lesson_note/', null=True, blank=True)
    
    status = models.BooleanField(default=True)
    is_admin_aproved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lesson_name
    
class Assignment_Submission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    assignment = models.FileField(upload_to='assignment_submission/')
    marks = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.student.username + ' - ' + self.lesson.lesson_name


class Exams(models.Model):
    exam_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True)
    Chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE,null=True, blank=True)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE,null=True, blank=True)
    exam_date = models.DateField()
    exam_time = models.TimeField( null=True, blank=True)
    exam_duration = models.IntegerField(default=0, null=True, blank=True)
    exam_link = models.URLField(null=True, blank=True)
    is_mcq = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    is_admin_aproved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam_name

class Questions(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100)
    marks = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam.exam_name + ' - ' + self.question

class StudentAnswer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    marks = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.username + ' - ' + self.exam.exam_name + ' - ' + self.question.question
    






class CourseEnrollApplication(models.Model):
    course = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    status = models.BooleanField(default=False)

    payment_status = models.BooleanField(default=False)
    is_admin_aproved = models.BooleanField(default=True)

    payment_details = models.TextField(null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.course.subject_name +' '+ self.student.email
    