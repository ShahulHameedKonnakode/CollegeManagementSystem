from django.shortcuts import render,redirect, get_object_or_404
from main.forms import StudentData,TeacherData, DepartmentData
from django.http import HttpResponse
from main.models import Student,Staff, Department, Course,Mark,Subject,Examination,ExaminationSchedule,User,StaffRole, StaffAttendance,StudentAttendance,ExaminationGroup,Sessions,Book
from django.core.mail import send_mail
from CollegeManagementSystem import settings
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Prefetch
from main.decorators import teacher_required
# Create your views here.



@teacher_required
@login_required
@never_cache
def teacher_home(request):
    staff_id=request.session.get("teacher_id")
    staff_pic=Staff.objects.get(staff_id_id=staff_id)
    staff_count=Staff.objects.count()
    student_count=Student.objects.count()
    department_count=Department.objects.count()
    course_count=Course.objects.count()
    return render(request, 'teacher_home.html',{"profile":staff_pic,'staff_count':staff_count,'staff_id':staff_id,'student_count':student_count,'department_count':department_count,'course_count':course_count})

@teacher_required
@login_required
@never_cache
def edit_staff_profile(request, uid):
    logged_staff=request.session.get("teacher_id")
    data= Staff.objects.get(id=uid)
    department = Department.objects.all()
    if data.staff_id_id != logged_staff:
        messages.error(request, "You can only edit your own profile")
        return redirect('teacher_home')
    return render(request, 'edit_staff_profile.html',{"data":data, 'department':department})
 

# staff logging accessable pages
@login_required
@never_cache
def view_std_staff(request):
    std_data = Student.objects.all()     

    return render(request, 'viewstd_staff.html',{'studentdata': std_data})
    
@login_required
@never_cache
def view_staff_staff(request):
    staff_data = Staff.objects.all()
    return render(request, 'view_staff_staff.html',{'staffdata':staff_data})

@login_required
@never_cache
def view_course_staff(request):
    course_data=Course.objects.all()
    return render(request, 'view_course_staff.html',{'course_data':course_data})

def view_subject_staff(request):
    subject_data=Subject.objects.all()
    return render(request,'view_subject_staff.html',{'subject_data':subject_data})

def mark_student_attendance_staff(request):
    student_list = Student.objects.all()
    today = date.today()
    return render(request, 'mark_student_attendance_staff.html', {
            'students': student_list,
            'today': today
        })

def view_staff_attendance_staff(request):
    attendance_list = StaffAttendance.objects.all().order_by('-date')
    return render(request, 'view_staff_attendance_staff.html', {
        'attendance_list': attendance_list
    })

def view_student_attendance_staff(request):
    attendance_list = StudentAttendance.objects.all().order_by('-date')
    return render(request, 'view_student_attendance_staff.html', {
        'attendance_list': attendance_list
    })


def view_examination_schedule_staff(request):
    examination_schedule = ExaminationSchedule.objects.all().order_by('id')
    exam_group_data = ExaminationGroup.objects.all()
    exam_data = Examination.objects.all()
    
    
    
        
    return render(request,'view_examination_schedule_staff.html',
                  {'examination_schedule': examination_schedule,
        'exam_group_data': exam_group_data,
        'exam_data': exam_data})

def mark_entry_staff(request):
    exam_schedule = ExaminationSchedule.objects.all()
    students = Student.objects.all()
    
    if request.method == 'POST':
        # Process the submitted marks
        for student in students:
            for subject in exam_schedule:
                mark_field = f'mark_{student.id}_{subject.id}'
                grade_field = f'grade_{student.id}_{subject.id}'
                
                mark = request.POST.get(mark_field)
                grade = request.POST.get(grade_field)
                
                if mark:  # Only save if mark is provided
                    try:
                        # Convert mark to integer
                        mark = int(mark)
                        
                        # Get or create the student mark record
                        student_mark, created = Mark.objects.get_or_create(
                            student_id=student,
                            exam_schedule=subject,  # Note: Using exam_schedule instead of subject
                            defaults={
                                'mark': mark,
                                'grade': grade,
                            }
                        )
                        
                        if not created:
                            # Update existing record
                            student_mark.mark = mark
                            student_mark.grade = grade
                            student_mark.save()
                    
                    except ValueError:
                        messages.error(request, f"Invalid mark entered for {student.student_id.get_full_name()} in {subject.exam_subject.subject_name}")
                        continue
        
        messages.success(request, 'Marks saved successfully!')
        return redirect('mark_entry_staff')
    
    # For GET request - prepare existing marks data
    marks_data = {}
    existing_marks = Mark.objects.filter(
        student_id__in=[s.id for s in students],
        exam_schedule__in=[es.id for es in exam_schedule]
    ).select_related('student_id', 'exam_schedule')
    
    for mark in existing_marks:
        key = f"{mark.student_id.id}_{mark.exam_schedule.id}"
        marks_data[key] = {
            'mark': mark.mark,
            'grade': mark.grade
        }
    
    context = {
        'exam_schedule': exam_schedule,
        'students': students,
        'marks_data': marks_data,
    }
    return render(request, 'mark_entry_staff.html', context)


@require_GET
def result_staff(request):
    # Get all distinct subjects
    subjects = ExaminationSchedule.objects.all().select_related('exam_subject')
    
    # Get all students with their marks
    students = Student.objects.select_related('student_id').prefetch_related(
        Prefetch('mark_set', queryset=Mark.objects.select_related('exam_schedule'))
    ).all()
    
    # Organize data
    student_data = []
    for student in students:
        results = {mark.exam_schedule.id: {'mark': mark.mark, 'grade': mark.grade} 
                  for mark in student.mark_set.all()}
        student_data.append({
            'student_obj': student,
            'results': results
        })
    
    context = {
        'subjects': subjects,
        'students': student_data,
    }
    return render(request, 'result_staff.html', context)



def view_library_book_staff(request):
    books=Book.objects.all()
    return render(request, 'view_library_book_staff.html',{'books':books})