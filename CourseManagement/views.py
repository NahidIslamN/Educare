from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Authentication.models import CustomUser
from CourseManagement.models import *
import datetime 

from django.contrib import messages

#####
#delete media file
import os
from django.conf import settings
# Create your views here.


class CourseView(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_superuser:
            teachers = CustomUser.objects.filter(is_teacher=True)


            courses = Subjects.objects.all().order_by('-created_at')



            cp={
                "active_id":"a003",
                "teachers":teachers,
                'courses':courses
            }
            return render(request, "course.html", context=cp)
        else:
            return redirect("/")
    
    
    @method_decorator(login_required)
    def post(self, request):
        if request.user.is_superuser:
            method = request.POST.get('_method', '').upper()
            if method == "ADDCOURSE":
                data = request.POST
                img = request.FILES.get('subject_image')

                if Subjects.objects.filter(subject_name=data.get('subject_name')).exists():

                    cp = {
                        'icon':'warning',
                        'title':"Course Already Exists!",
                        'text': "The course with this name already exists in the database!"
                        }
                    return render(request,'alarts.html', context=cp)
                else:
                    teacher = CustomUser.objects.get(id = data.get('teacher_id'))
                    course = Subjects.objects.create(
                        subject_name=data.get('subject_name'),
                        subject_description=data.get('subject_description'),
                        course_enrole_fee=data.get('course_enrole_fee'),
                        senester_rank=data.get('senester_rank'),
                        teacher= teacher,
                        subject_image=img,
                        is_admin_aproved=True
                    )
                    course.save()
                    cp = {
                        'icon':'success',
                        'title':"Course Added!",
                        'text': "The course has been added successfully!"
                    }
                    return render(request,'alarts.html', context=cp)  
            
                
            
            else:
                # Waiting for the next operation
                pass
            
              
        else:
            return redirect("/")


class CourseDetails(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_superuser:
            teachers = CustomUser.objects.filter(is_teacher=True)
            course_id = None
            try:
                course_id = Subjects.objects.get(id = request.GET.get('cid'))
            except:
                cp = {
                    'icon':'warning',
                    'title':"Course Already Exists!",
                    'text': "The course with this name already exists in the database!"
                    }
                return render(request,'alarts.html', context=cp)
            
            cp = {
                "active_id":"a003",
                'subject':course_id,
                'teachers':teachers
            }
            return render(request,'coursedetails.html', context=cp)
    

    @method_decorator(login_required)
    def post(self, request):
        if request.user.is_superuser:
            data = request.POST
            image = request.FILES.get('subject_image')

            status = None
            admin_aprove = None

            try:
                status = data.get('status')
            except:
                pass

            try:
                admin_aprove = data.get('admin_aprove')
            except:
                pass
            # print(data)
            # print(image)

            subject_id = int(data.get("subject_id")) 
            teacher_id = int(data.get('teacher_id'))
            teachers = CustomUser.objects.get(id = teacher_id)
            edite_subject = Subjects.objects.get(id = subject_id)

            course_enrole_fee = float(data.get('course_enrole_fee'))

            edite_subject.subject_name = data.get('subject_name')

            edite_subject.course_enrole_fee = course_enrole_fee

            edite_subject.senester_rank = data.get('senester_rank')

            if edite_subject.teacher == teachers:
                pass
            else:
                edite_subject.teacher = teachers

            edite_subject.subject_description = data.get('subject_description')


            if status:
                edite_subject.status = True
            else:
                edite_subject.status = False

            if admin_aprove:
                edite_subject.is_admin_aproved = True
            else:
                edite_subject.is_admin_aproved = False
            

            if image:
                file_path = edite_subject.subject_image.path
                os.remove(file_path)
                edite_subject.subject_image = image

            edite_subject.save()
            
        

                
            cp = {
                'icon':'success',
                'title':"Course Edited!",
                'text': "The course has been edited successfully!"
            }
            return render(request,'alarts.html', context=cp)
        








#### Teacher works here######


class MyCourses(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_teacher or request.user.is_superuser:

            if request.user.is_superuser:
                my_courses = Subjects.objects.all().order_by('-created_at')
            else:
                my_courses = Subjects.objects.filter(is_admin_aproved = True, status = True, teacher = request.user).order_by('-created_at')

            cp = {
             "active_id":"t001",
             'my_courses':my_courses               
            }
            return render (request,'teachers/courses.html', context=cp)


class CoursesDetails(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_teacher or request.user.is_superuser:
            my_course = None
            
            try:
                my_course = Subjects.objects.get(id = request.GET.get('cid'))
                chapters = Chapters.objects.filter(status = True, is_admin_aproved = True, subject = my_course)
                chapter_with_lesson = [[i, Lessons.objects.filter(chapter = i),] for i in chapters] 
                
                
            except:
                pass

            course_students = CourseEnrollApplication.objects.filter(course = my_course ).order_by('-create_at')



            
            

            if my_course and request.user.is_superuser:
                chapters = Chapters.objects.all()
                cp = {
                "active_id":"t001",
                'my_course':my_course,
                "chapter_with_lesson":chapter_with_lesson
                             
                }
                return render(request, 'teachers/course_details.html', context=cp)
            elif my_course and my_course.is_admin_aproved and my_course.status and my_course.teacher == request.user :                 

                cp = {
                "active_id":"t001",
                'my_course':my_course,
                'chapter_with_lesson':chapter_with_lesson,
                "cs":course_students
                             
                }
                return render(request, 'teachers/course_details.html', context=cp)
            else:
                cp = {
                'icon':'warning',
                'title':"Somthing want to be worng!",
                'text': "Try again later!"
            }
            return render(request,'alarts.html', context=cp)
        cp = {
            'icon':'warning',
            'title':"Somthing want to be worng!",
            'text': "Try again later!"
        }
        return render(request,'alarts.html', context=cp)
    
    @method_decorator(login_required)
    def post(self,request):
        if request.user.is_teacher or request.user.is_superuser:
            method = request.POST.get('_method', '').upper()
            data = request.POST


            if method == "CHAPTERCREATE":
                chapter_plan = request.FILES.get('chapter_plan')

                subject = Subjects.objects.get(id = data.get('subject_id'))
                if subject.teacher == request.user or request.user.is_superuser :
                    chapter = Chapters.objects.create(
                        chapter_name = data.get('chapter_name'),
                        subject = subject,
                    )
                    if chapter_plan:
                        chapter.chapter_plan = chapter_plan
                    
                    chapter.save()
                    cp = {
                        'icon':'success',
                        'title':"Successfully Create Chapter!",
                        'text': "go to your chapter section!"
                    }
                    return render(request,'alarts.html', context=cp)

            elif method == "CHAPTELESSON":
                chapter_id = Chapters.objects.get(id = data.get('chapter_id'))
                lesson_name = data.get('lesson_name')
                les = Lessons.objects.create(
                    lesson_name = lesson_name,
                    chapter = chapter_id,
                )
                les.save()
                
                cp = {
                    'icon':'success',
                    'title':"Successfully Create Lesson!",
                    'text': "Thank you create a lesson for student!"
                }
                return render(request,'alarts.html', context=cp)

            elif method == 'UPDATELESSON':
                lesson_id = None
                try:
                    lesson_id = Lessons.objects.get(id = data.get('lesson_id'))
                except:
                    pass
                

                if lesson_id and lesson_id.chapter.subject.teacher == request.user:
                    print(data)

                    assignment = request.FILES.get('assignment')
                    lesson_video = request.FILES.get('lesson_video')
                    lesson_resource = request.FILES.get('lesson_resource')


                    if assignment:                        
                        if lesson_id.assignment:
                            file_path = lesson_id.assignment.path
                            os.remove(file_path)
                            lesson_id.assignment = assignment
                            lesson_id.save()

                        else:
                            lesson_id.assignment = assignment
                            lesson_id.save()
                    
                    if lesson_video:                        
                        if lesson_id.lesson_video:
                            file_path = lesson_id.lesson_video.path
                            os.remove(file_path)
                            lesson_id.lesson_video = lesson_video
                            lesson_id.save()

                        else:
                            lesson_id.lesson_video = lesson_video
                            lesson_id.save()
                    
                    if lesson_resource:
                        
                        if lesson_id.resource_file:
                            file_path = lesson_id.resource_file.path
                            os.remove(file_path)
                            lesson_id.resource_file = lesson_resource
                            lesson_id.save()

                        else:
                            lesson_id.resource_file = lesson_resource
                            lesson_id.save()
                    
                    lesson_id.lesson_name = data.get('lesson_name')
                    lsat_date_of_submission = data.get('lsat_date_of_submission')
                    if lsat_date_of_submission:
                        lesson_id.lsat_date_of_submission = lsat_date_of_submission
                    
                    live_class_link = data.get('live_class_link')

                    if live_class_link:
                        lesson_id.live_class_link = live_class_link
                    
                    live_class_date = data.get('live_class_date')
                    if live_class_date:
                        lesson_id.live_class_date = live_class_date
                    

                    lesson_video = data.get('lesson_video')
                    if lesson_video:
                        lesson_id.lesson_video = lesson_video
                    
                    iframe_data = data.get('iframe_data')
                    if iframe_data:
                        lesson_id.iframe_data = iframe_data
                    
                    lesson_id.save()                   
                    
                    cp = {
                        'icon':'success',
                        'title':"Course Updated!",
                        'text': "The course has been updated successfully!"
                    }
                    return render(request,'alarts.html', context=cp) 
                else:

                    cp = {
                        'icon':'warning',
                        'title':"You can't Update it!",
                        'text': "You are not the teacher of this course!"
                    }
                    return render(request,'alarts.html', context=cp) 

                
            elif method == "CHAPTERUPDATE":
                chapter_plan = request.FILES.get('chapter_plan')
                try:
                    chapter = Chapters.objects.get(id = data.get('chapter_id'))
                except:
                    cp = {
                        'icon':'warning',
                        'title':"Chapter not found!",
                        'text': "pleace check the chapter is present!"
                    }
                    return render(request,'alarts.html', context=cp)
                    
                if chapter.subject.teacher == request.user or request.user.is_superuser :
                    if chapter_plan:
                        file_path = chapter.chapter_plan.path
                        os.remove(file_path)
                        chapter.chapter_plan = chapter_plan
                    
                    chapter.chapter_name = data.get('chapter_name')
                    chapter.number_of_lessons = data.get('number_of_lessons')
                    chapter.save()

                     
                    cp = {
                        'icon':'success',
                        'title':"Successfully Update Chapter!",
                        'text': "go to your chapter section!"
                    }
                    return render(request,'alarts.html', context=cp)
            
            elif method == "APPLACATIONACCEPT":
                status = data.get("status")
                application = CourseEnrollApplication.objects.get(id = data.get('application_id'))
                subjects = application.course
                if status:                    
                    application.status = True
                    application.payment_status = True
                    subjects.students.add(application.student)
                    subjects.save()
                    application.save()
                    return redirect(f'/courses/courses-teachers/details/?cid={application.course.id}')
                else:
                    application.status = False
                    application.payment_status = False
                    subjects.students.remove(application.student)
                    subjects.save()
                    application.save()
                    return redirect(f'/courses/courses-teachers/details/?cid={application.course.id}')
                    
            else:
                pass             

           


            return redirect(f'/courses/courses-teachers/details/?cid={data.get('subject_id')}')

        return redirect('/')

       


class ExamsTeachers(View):
    @method_decorator(login_required)
    def get(self, request):

        if request.user.is_teacher:  
            exams = Exams.objects.filter(subject__teacher = request.user)

            exam_with_questions = [[i, Questions.objects.filter(exam = i),] for i in exams]
            all_subjects = Subjects.objects.filter(teacher = request.user).order_by('-created_at')
            
            cp={
                "active_id":"t002",
                'exams':exams,
                "all_subjects":all_subjects,
                'exam_with_questions':exam_with_questions
            }
            return render(request,'teachers/exams.html', context=cp)
        
    @method_decorator(login_required)
    def post(self, request):
        method = request.POST.get('_method', '').upper()
        data = request.POST
        if method == "ANSWERSUBMIT":
            print(data)
            cp = {
                'icon':'success',
                'title':"Successfull!",
                'text': "Answer Submit Successfull!"
            }
            return render(request,'alarts.html', context=cp)
        elif method == "EXAMCREAT":

            if request.user.is_teacher: 
                try:
                    chapter_id = Subjects.objects.get(id = data.get('chapter_id'))
                except:
                    return redirect('/')
                
                exams = Exams.objects.create(
                    exam_name = data.get('exam_name'),
                    subject = chapter_id,
                    exam_date = data.get('date'),
                    status = False,
                )
                exams.save()   
                cp = {
                    'icon':'success',
                    'title':"Exam Created Successfully!",
                    'text': "Exam created successfully! student will get the exam when status is on!"
                }
                return render(request,'alarts.html', context=cp)
            
            else:
                return redirect('/')
        

        elif method == "CHAPTEQUESTION":
            try:
                exam = Exams.objects.get(id = data.get('exam_id'))
            except:
                return redirect('/')
            if request.user.is_teacher:

                question = Questions.objects.create(
                    exam = exam,
                    question = data.get('question'),
                    option1 = data.get('opt1'),
                    option2 = data.get('opt2'),
                    option3 = data.get('opt3'),
                    option4 = data.get('opt3'),
                    correct_option = data.get('currect_answer'),
                    marks = data.get('mark'),          

                )
                question.save()
                
                cp = {
                    'icon':'success',
                    'title':"Question Created Successfully!",
                    'text': "Student will get the question!"
                }
                return render(request,'alarts.html', context=cp)

          
            return redirect('/')
        
        elif method == "EXAMUPDATE":
           
            try:
                exam_id = Exams.objects.get(id = data.get('exam_id')) 
            except:
                return redirect('/')           
            subject_id= Subjects.objects.get(id = data.get('subject_id'))
            if exam_id.subject.teacher == request.user:
                exam_id.exam_name = data.get("exam_name")

                exam_id.subject = subject_id            
                
                if data.get('exam_date'):
                    exam_id.exam_date = data.get('exam_date')


                if data.get('exam_time'):
                    exam_id.exam_time = data.get('exam_time')


                if data.get('exam_duration'):
                    exam_id.exam_duration = data.get('exam_duration')

                    
                status = data.get('status')
                if status:
                    exam_id.status = True
                else:
                    exam_id.status = False
                

                exam_id.save()
                
                cp = {
                    'icon':'success',
                    'title':"Exam Update Successfully!",
                    'text': "Exma Update Successfully!"
                }
                return render(request,'alarts.html', context=cp)
            else:
                cp = {
                    'icon':'warning',
                    'title':"You are not the course teachers!",
                    'text': "Only Course Teacher can update the exam data!"
                }
                return render(request,'alarts.html', context=cp)

        else:
            return redirect('/')





###### Student views



class CoursesStudents(View):
    # @method_decorator(login_required)
    
    def get(self, request):
        try:
            users = request.user
            all_course = Subjects.objects.filter(senester_rank = users.semester).order_by('-created_at')
            cp = {
                'active_id':"s001",
                'all_course':all_course
            }
            return render(request, 'students/allcourse.html', context=cp)
        except:
            all_course = Subjects.objects.filter().order_by('-created_at')
            cp = {
                'active_id':"s001",
                'all_course':all_course
            }
            return render(request, 'students/public_courses.html', context=cp)
    
    @method_decorator(login_required)
    def post(self, request):
        method = request.POST.get('_method', '').upper()
        data = request.POST

        if method == "ENROLLMENT":
            try:
                student = request.user
                subject = Subjects.objects.get(id = data.get('subject_id'))
                

            except:
                cp = {
                    'icon':'info',
                    'title':"Something want to be worng",
                    'text': "Try again letter!"
                }
                return render(request,'alarts.html', context=cp)
            if CourseEnrollApplication.objects.filter(course = subject, student = student ).exists():
                cp = {
                    'icon':'warning',
                    'title':"You already applied",
                    'text': "teacher will aproved your application!"
                }
                return render(request,'alarts.html', context=cp)
            else:
            
                payment_info = data.get('payment_info')
                applicatioon =  CourseEnrollApplication(
                    course = subject,
                    student = student,
                    payment_details = payment_info,
                    
                    )
                applicatioon.save()
                cp = {
                    'icon':'success',
                    'title':"Application sent successfully",
                    'text': "Teacher will aproved your application!"
                }
                return render(request,'alarts.html', context=cp)

        else:
            pass

        return redirect('/courses/')

        # CourseEnrollApplication
       


class StudentEnrolledCourse(View):
    @method_decorator(login_required)
    def get(self, request):
        student = request.user

        # Assuming `student` is a CustomUser instance
        subjects = Subjects.objects.filter(students=student)



        cp = {
            "active_id":"s002",
            "subjects":subjects
        }
        return render(request, 'students/mycourses.html', context=cp)


class EnroledCourseDetails(View):
    @method_decorator(login_required)
    def get(self, request,pk):
        student = request.user
     
        my_course = None
        
        try:
            my_course = Subjects.objects.get(id = pk)
            exams = Exams.objects.filter(subject = my_course, status = True)
            exam_with_questions = [[i, Questions.objects.filter(exam = i),] for i in exams]
            if student in my_course.students.all():                
                chapters = Chapters.objects.filter(status = True, is_admin_aproved = True, subject = my_course)
                chapter_with_lesson = [[i, Lessons.objects.filter(chapter = i),] for i in chapters] 
            else:
                cp = {
                    'icon':'warning',
                    'title':"You have to enrolled first!",
                    'text': "Try again later!"
                }
                return render(request,'alarts.html', context=cp)    
        except:
            pass

       
            
        
        

        if my_course:
            chapters = Chapters.objects.all()
            cp = {
            "active_id":"s002",
            'my_course':my_course,
            "chapter_with_lesson":chapter_with_lesson,
            'today': datetime.date.today(),
            'exam_with_questions':exam_with_questions,
                            
            }
            return render(request, 'students/enroledcoursesdetails.html', context=cp)

    
    def post(self, request, pk):
        method = request.POST.get('_method', '').upper()
        if method == "ANSWERSUBMIT":
            data = request.POST
            print(data)
            return redirect('/')
        elif method == "ASSIGNMENTSUBMIT":
            student = request.user
            file = request.FILES.get('assignment_answer')
            try:
                lesson = Lessons.objects.get(id=pk)
                if Assignment_Submission.objects.filter(student = student, lesson = lesson ).exists():
                    cp = {
                        'icon':'warning',
                        'title':"Already Submit Assignment answer!",
                        'text': "Assignment answer already submit. Can't submit answer again!"
                    }
                    return render(request,'alarts.html', context=cp)
                    
                else:
                    a_s = Assignment_Submission.objects.create(
                        student = student,
                        lesson = lesson,
                        assignment = file
                    )
                    a_s.save()
                    cp = {
                        'icon':'success',
                        'title':"Successfully Submit Assignment!",
                        'text': "Assignment Submit Successfully. Teacher will view and makeing!"
                    }
                    return render(request,'alarts.html', context=cp)
                    

            except Lessons.DoesNotExist:
                pass
    
          
            return redirect(f'my-courses-student/{pk}/')
        else:
            return redirect (f'my-courses-student/{pk}/')
        




    
