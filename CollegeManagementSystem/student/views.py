from django.shortcuts import render,redirect, get_object_or_404
from main.forms import StudentData,TeacherData, DepartmentData
from django.http import HttpResponse, JsonResponse
from main.models import Student,Staff, Department, Course,Mark,Subject,Examination,ExaminationSchedule,User,StaffRole, StaffAttendance,StudentAttendance,ExaminationGroup,Sessions,Book
from student.models import StudentExamRegistration
from student.models import StudentExamRegistration
from django.core.mail import send_mail
from CollegeManagementSystem import settings
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Prefetch
from main.decorators import student_required


from django.urls import reverse

# Create your views here.
@student_required
@login_required
@never_cache
def student_home(request):
    student_id=request.session.get("student_id")
    student_pic=Student.objects.get(student_id_id=student_id)

    staff_count=Staff.objects.count()
    student_count=Student.objects.count()
    department_count=Department.objects.count()
    course_count=Course.objects.count()
    
    return render(request, 'student_home.html',{'profile':student_pic,'staff_count':staff_count,'student_count':student_count,'department_count':department_count,'course_count':course_count})


def view_course_student(request):
    course_data=Course.objects.all()
    return render(request, 'view_course_student.html',{'course_data':course_data})

def view_student_attendance_student(request):
    attendance_list = StudentAttendance.objects.all().order_by('-date')
    return render(request, 'view_student_attendance_student.html', {
        'attendance_list': attendance_list
    })



def view_examination_schedule_student(request):
    examination_schedule = ExaminationSchedule.objects.all().order_by('id')
    exam_group_data = ExaminationGroup.objects.all()
    exam_data = Examination.objects.all()    
    
        
    return render(request,'view_examination_schedule_student.html',
                  {'examination_schedule': examination_schedule,
        'exam_group_data': exam_group_data,
        'exam_data': exam_data})


@student_required
@login_required
@never_cache
def exam_registration(request):
    student_id = request.session.get("student_id")
    student = Student.objects.get(student_id=student_id)
    
    exam_group_data = ExaminationGroup.objects.all()
    exam_data = Examination.objects.all() 
    
    if request.method == 'POST':
        exam_group_id = request.POST.get('exam_group_id')
        exam_id = request.POST.get('exam_id')
        
        if exam_group_id:
            selected_exam_group = ExaminationGroup.objects.get(id=exam_group_id)
            exam_data = Examination.objects.filter(exam_group=selected_exam_group)
            
            if exam_id:
                selected_exam = Examination.objects.get(id=exam_id)
                examination_schedule = ExaminationSchedule.objects.filter(
                    exam_group=selected_exam_group,
                    exam_name=selected_exam
                )
                
                # Handle registration if needed
                if 'register' in request.POST:
                    selected_subjects = request.POST.getlist('selected_subjects')
                    if selected_subjects:
                        registration = StudentExamRegistration.objects.create(
                            student=student,
                            exam=selected_exam
                        )
                        registration.subjects.set(selected_subjects)
                        messages.success(request, "Registration successful!")
                        return redirect('exam_registration')
    
    return render(request, 'exam_registration.html', {
        'student': student,
        'exam_group_data': exam_group_data,
        'exam_data': exam_data
        # 'selected_exam_group': selected_exam_group,
        # 'selected_exam': selected_exam
        
    })
@student_required
@login_required
@never_cache
def get_exam_schedule(request,eid):
    examination_schedule =ExaminationSchedule.objects.filter(exam_group_id=eid)
    
    return render(request, 'exam_registration.html', {
    
        'examination_schedule': examination_schedule
    })

def result_student(request):
    # Get student ID from session
    student_id = request.session.get('student_id')
    if not student_id:
        # Handle case where student is not logged in
        return redirect('logins')  # or appropriate error handling
    
    # Get all distinct subjects
    subjects = ExaminationSchedule.objects.all().select_related('exam_subject')
    
    # Get only the logged-in student with their marks
    try:
        student = Student.objects.select_related('student_id').prefetch_related(
            Prefetch('mark_set', queryset=Mark.objects.select_related('exam_schedule'))
        ).get(id=student_id)
    except Student.DoesNotExist:
        # Handle case where student doesn't exist
        return redirect('logins')  # or appropriate error handling
    
    # Organize data for just this student
    results = {mark.exam_schedule.id: {'mark': mark.mark, 'grade': mark.grade} 
              for mark in student.mark_set.all()}
    
    context = {
        'subjects': subjects,
        'student': {  # Changed from students (plural) to student (singular)
            'student_obj': student,
            'results': results
        },
    }
    return render(request, 'result_student.html', context)



def view_library_book_student(request):
    books=Book.objects.all()
    return render(request, 'view_library_book_student.html',{'books':books})