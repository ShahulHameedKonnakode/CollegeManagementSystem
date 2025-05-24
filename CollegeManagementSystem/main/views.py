from django.shortcuts import render,redirect, get_object_or_404
from main.forms import StudentData,TeacherData, DepartmentData, LibraryData
from django.http import HttpResponse
from main.models import Student,Staff, Department, Course,Mark,Subject,Examination,ExaminationSchedule,User,StaffRole, StaffAttendance,StudentAttendance,ExaminationGroup,Sessions,LibraryBookCategory,Book
from django.core.mail import send_mail
from CollegeManagementSystem import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from main.decorators import admin_required,teacher_required
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.db.models import Prefetch

from django.contrib.admin.views.decorators import staff_member_required


from datetime import date


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import *
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

def export_attendance_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Set document title
    p.setTitle("Staff Attendance Report")
    
    # Add title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Staff Attendance Report")
    
    # Get attendance data
    attendance_list = StaffAttendance.objects.all().order_by('-date')
    
    # Prepare data for table
    data = [["No.", "Date", "Staff Name", "Department", "Status", "Notes"]]
    
    for i, record in enumerate(attendance_list, 1):
        data.append([
            str(i),
            record.date.strftime("%Y-%m-%d"),
            record.staff.staff_id.get_full_name(),
            record.staff.department_id.dep_name,
            record.get_status_display(),
            record.notes or "-"
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    # Draw table on PDF
    table.wrapOn(p, 400, 600)
    table.drawOn(p, 100, 600)
    
    # Close the PDF object cleanly
    p.showPage()
    p.save()
    
    # File response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="staff_attendance.pdf"'
    
    return response



# logins

def logins(request):
    if request.method=='POST':
        user_name=request.POST['uname']
        pass_word=request.POST['password']
        user=authenticate(request, username=user_name, password=pass_word)

        if user is not None and user.is_superuser==1:
            login(request, user)
            return redirect(admin_home)
        elif user is not None and user.user_type=='Teacher':
            login(request, user)
            request.session['teacher_id']=user.id
            return redirect(reverse('staff:teacher_home'))

        elif user is not None and user.user_type=='student' and user.is_active==1:
            login(request, user)
            request.session['student_id']=user.id
            return redirect(reverse('student:student_home'))

    return render(request, 'logins.html')

# @login_required
# @never_cache
def logouts(request):
    request.session.flush()
    logout(request)

    return redirect(index)


# home
def index(request):
    teacher_data = Staff.objects.all()
    return render(request, 'index.html', {'teacher':teacher_data})


# sessions
@admin_required
@login_required
@never_cache
def add_session(request):
    if request.method == 'POST':
        session=request.POST['session_name']
        session_data=Sessions.objects.create(session_name=session)
        session_data.save()
        messages.warning(request,"Session Successfully Added")
        return redirect(admin_home)
    return render(request, 'add_session.html')
# Departement
@admin_required
@login_required
@never_cache
def add_department(request):
    if request.method == 'POST':
        department_name=request.POST['dep_name']
        department_data=Department.objects.create(dep_name=department_name)
        return HttpResponse("<script>window.alert('Department Added Successfully!'); window.location.href='view_department'</script>")
    else:
        return render(request, 'add_department.html')

@admin_required
@login_required
@never_cache
def view_department(request):
    department_data=Department.objects.all()
    return render(request, 'view_department.html',{'department_data':department_data})

@admin_required
@login_required
@never_cache
def edit_department(request,eid):
    edit_data=Department.objects.get(id=eid)
    return render(request, 'edit_department.html',{'edit_dep_data':edit_data})


@admin_required
@login_required
@never_cache
def update_department(request,uid):
    update_date=get_object_or_404(Department,id=uid)
    if request.method == 'POST':
        form=DepartmentData(request.POST)
        if form.is_valid():
            update_date.dep_name=form.cleaned_data['dep_name']
            update_date.save()
            return redirect(view_department)


@login_required
@never_cache
def delete_department(request, did):
    delete_data=Department.objects.get(id=did)
    delete_data.delete()
    messages.warning(request, "Are You Sure?!")
    return redirect(view_department)


# Course
@admin_required
@login_required
@never_cache
def add_course(request):

    if request.method=='POST':
        department_id=request.POST['dep_id']
        course_code=request.POST['course_code']
        course_name=request.POST['course_name']
        course_data=Course.objects.create(department_id=department_id,course_code=course_code,course_name=course_name)
        course_data.save()
        messages.warning(request,"Course Successfully Added")
        return redirect(view_course)
    else:
        department_data=Department.objects.all()
        return render(request, 'add_course.html',{"departement_data":department_data})

@admin_required
@login_required
@never_cache
def view_course(request):
    course_data=Course.objects.all()
    return render(request, 'view_course.html',{'course_data':course_data})

@admin_required
@login_required
@never_cache
def edit_course(request,eid):
    if request.method=='GET':
        course_to_edit=Course.objects.get(id=eid)
        departments=Department.objects.all()
        return render(request, 'edit_course.html',{'course_to_edit':course_to_edit,'departments':departments})
    elif request.method=='POST':
        course_code=request.POST['course_code']
        course_name=request.POST['course_name']
        course_dep=request.POST['dep_id']
        course_to_update=Course.objects.filter(id=eid).update(course_code=course_code,course_name=course_name,department_id=course_dep)        
        return redirect(view_course)
    
@admin_required
@login_required
@never_cache
def delete_course(request,did):
    course_to_delete=Course.objects.get(id=did)
    course_to_delete.delete()
    messages.warning(request, "Are You Sure?!")
    return redirect(view_course)

#Subject
@admin_required
@login_required
@never_cache
def add_subject(request):
    if request.method=='POST':
        course_id=request.POST['course_id']
        subject_code=request.POST['subject_code']
        subject_name=request.POST['subject_name']
        subject_data=Subject.objects.create(course_id=course_id,subject_code=subject_code,subject_name=subject_name)
        subject_data.save()
        messages.warning(request,"Subject Added Successfully!")
        return redirect(view_subject)
    else:
        course_data=Course.objects.all()
        return render(request, 'add_subject.html',{'course_data':course_data})

@admin_required
@login_required
@never_cache    
def view_subject(request):
    subject_data=Subject.objects.all()
    return render(request,'view_subject.html',{'subject_data':subject_data})

@admin_required
@login_required
@never_cache
def edit_subject(request,eid):
    if request.method == 'GET':
        subject_to_edit=Subject.objects.get(id=eid)
        course_data=Course.objects.all()
        return render(request,'edit_subject.html',{'subject_to_edit':subject_to_edit, 'course_data':course_data})
    elif request.method =='POST':
        course_id=request.POST['subject_id']
        subject_code=request.POST['subject_code']
        subject_name=request.POST['subject_name']
        subject_to_update=Subject.objects.filter(id=eid).update(course_id=course_id,subject_code=subject_code,subject_name=subject_name)
        return redirect(view_subject)


@admin_required
@login_required
@never_cache
def delete_subject(request,did):
    subject_to_delete=Subject.objects.get(id=did)
    subject_to_delete.delete()
    messages.warning(request, "Are You Sure?!")
    return redirect(view_subject)

# Examination
@admin_required
@login_required
@never_cache
def create_examination_group(request):
    if request.method=='POST':
        exam_group_name=request.POST['name']
        description=request.POST['description']
        examination_group=ExaminationGroup.objects.create(exam_group_name=exam_group_name,description=description)
        examination_group.save()
        messages.warning(request, "Examintation Created Successfully!")
        return redirect(view_examination)
    return render(request,'create_examination_group.html')

@admin_required
@login_required
@never_cache
def create_examination(request):
    if request.method=='POST':
        exam_group=request.POST['exam_group_id']
        exam_session=request.POST['session_name']
        exam_name=request.POST['name']
        exam_description=request.POST['description']
        examination=Examination.objects.create(name=exam_name,description=exam_description,exam_group_id=exam_group,session_id=exam_session)
        examination.save()
        messages.warning(request, "Examintation Created Successfully!")
        return redirect(view_examination)
    exam_group_data=ExaminationGroup.objects.all()
    exam_session_data=Sessions.objects.all()
    return render(request, 'create_examination.html',{'exam_group_data':exam_group_data,'exam_session_data':exam_session_data})


@admin_required
@login_required
@never_cache
def view_examination(request):
    exam_data=Examination.objects.all()
    return render(request, 'view_examination.html',{'exam_data':exam_data})


@admin_required
@login_required
@never_cache
def edit_examination(request,eid):
    pass


@admin_required
@login_required
@never_cache
def delete_examination(request,did):
    pass

#Examintaion Schedule
@admin_required
@login_required
@never_cache
def create_examination_schedule(request):
    if request.method == 'POST':
        exam_group=request.POST['exam_group_id']
        exam_id=request.POST['exam_id']
        exam_subject=request.POST['subject_id']
        exam_date=request.POST['exam_date']
        exam_time=request.POST['exam_time']
        room_no=request.POST['room_no']
        min_mark=request.POST['min_mark']
        max_mark=request.POST['max_mark']
        exam_schedule=ExaminationSchedule.objects.create(exam_group_id=exam_group,exam_name_id=exam_id, exam_subject_id=exam_subject,exam_date=exam_date, exam_time=exam_time,room_no=room_no,min_mark=min_mark, max_mark=max_mark)
        exam_schedule.save()
        return redirect(create_examination_schedule)
    else:
        subject_data=Subject.objects.all()
        exam_group_data=ExaminationGroup.objects.all()
        exam_data=Examination.objects.all()
        examination_schedule=ExaminationSchedule.objects.all()
        return render(request,'examination_schedule.html',{'subject_data':subject_data,'examination_schedule1':examination_schedule,'exam_group_data':exam_group_data, 'exam_data':exam_data})



@admin_required
@login_required
@never_cache

def view_examination_schedule(request):
    examination_schedule = ExaminationSchedule.objects.all().order_by('id')
    exam_group_data = ExaminationGroup.objects.all()
    exam_data = Examination.objects.all()
    
    if request.method == 'POST':
        exam_group_id = request.POST.get('exam_group_id')
        exam_id = request.POST.get('exam_id')
        
        if exam_group_id:
            examination_schedule = examination_schedule.filter(exam_group_id=exam_group_id)
            selected_exam_group = ExaminationGroup.objects.get(id=exam_group_id)
        if exam_id:
            examination_schedule = examination_schedule.filter(exam_name_id=exam_id)
            selected_exam = Examination.objects.get(id=exam_id)
    
    return render(request, 'view_examination_schedule.html', {
        'examination_schedule': examination_schedule,
        'exam_group_data': exam_group_data,
        'exam_data': exam_data,
        # 'selected_exam_group': selected_exam_group,
        # 'selected_exam': selected_exam
    })


def mark_entry(request):
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
        return redirect('mark_entry')
    
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
    return render(request, 'mark_entry.html', context)


@require_GET
def result(request):
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
    return render(request, 'result.html', context)

#admin
@admin_required
# @staff_member_required
def admin_home(request):
    staff_data=Staff.objects.all()
    staff_count=Staff.objects.count()
    student_count=Student.objects.count()
    department_count=Department.objects.count()
    course_count=Course.objects.count()
    
    return render(request, 'admin_home.html',{'staff_data':staff_data,'staff_count':staff_count,'student_count':student_count,'department_count':department_count,'course_count':course_count})

@admin_required
# @staff_member_required
@login_required
@never_cache
def admin_approve_students(request,aid):
    student_to_approve=Student.objects.get(id=aid)
    student_to_approve.student_id.is_active=True
    student_to_approve.student_id.save()
    return redirect(view_std)
# Student Related Functions



@login_required
@never_cache
def SendEmail(email, name,request=None):
    sub="welcome"
    message=f"Hi {name},\n You Have been Successfully Entrolled. \n Thank You!"    
    send_mail(sub,message,settings.EMAIL_HOST_USER,[email])


@admin_required
@login_required
@never_cache
def add_student(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email= request.POST['email']
        mob=request.POST['mob']
        course= request.POST['course_id']
        photo= request.FILES['photo']
        print(first_name,last_name,username,password,email,mob,course,photo)
        student_user= User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email,user_type='student',is_active=False)
        student_user.save()
        student_datas=Student.objects.create(student_id=student_user,mob=mob,course_id=course,photo=photo)
        student_datas.save()
        
        # SendEmail(email,first_name)
            
        return HttpResponse("<script>window.alert('Student Entrolled Successfully!'); window.location.href='view_std'</script>")
    
    course_data=Course.objects.all() 
        
    return render(request, 'add_student.html',{"course_data":course_data})


@admin_required
@login_required
@never_cache
def view_std(request):

    std_data = Student.objects.all()     

    return render(request, 'viewstd.html',{'studentdata': std_data})

@admin_required
@login_required
@never_cache
def edit_std(request, eid):
    std_data = Student.objects.get(id=eid)
    return render(request, 'edit_student.html',{'std_data':std_data})


@login_required
@never_cache
def update_std(request, uid):
    if request.method == 'POST':
        value = Student.objects.get(id=uid)
        form1 = StudentData(request.POST, request.FILES, instance=value)
        if form1.is_valid():
            form1.save()
            return redirect(view_std)
        return HttpResponse("Not Valid")
    return HttpResponse("No Data Found")



@admin_required
@login_required
@never_cache
def delete_std(request, did):
    delete_data=Student.objects.get(id=did)
    delete_data.delete()
    return redirect(view_std)



# student attendance

@admin_required
@login_required
@never_cache
def mark_student_attendance(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        today = date.today()
        
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            status = request.POST.get(f'status_{student_id}')
            notes = request.POST.get(f'notes_{student_id}', '')
            
            # Check if attendance already exists for today
            attendance, created = StudentAttendance.objects.get_or_create(
                student=student,
                date=today,
                defaults={
                    'status': status,
                    'notes': notes
                }
            )
            
            if not created:
                attendance.status = status
                attendance.notes = notes
                attendance.save()
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect(view_student_attendance)
    
    else:
        student_list = Student.objects.all()
        today = date.today()
        return render(request, 'mark_student_attendance.html', {
            'students': student_list,
            'today': today
        })

@admin_required
@login_required
@never_cache
def view_student_attendance(request):
    attendance_list = StudentAttendance.objects.all().order_by('-date')
    return render(request, 'view_student_attendance.html', {
        'attendance_list': attendance_list
    })


# staff related functions

@login_required
@never_cache
def add_staff(request):
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            email= request.POST['email']

            role_id=request.POST['role_id']
            role= StaffRole.objects.get(id=role_id) 


            mob=request.POST['mob']
            department= request.POST['dep_id']                      
            qualification=request.POST['qualification']
            photo= request.FILES['photo']
            staff_user_data=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email,user_type=role.role)
            staff_user_data.save()
            staff_data = Staff.objects.create(mob=mob,department_id_id=department, qualification=qualification,photo=photo,staff_id=staff_user_data)
            staff_data.save()      
        
            # SendEmail(email, first_name,request)
            messages.warning(request,'Teacher is Added Successfully!')
            return redirect(view_staff)
            # return HttpResponse("<script>window.alert('Teacher is Added Successfully!'); window.location.href='view_teacher'</script>")
        
    else:
        department_data=Department.objects.all()
        staff_role=StaffRole.objects.all()

        return render(request, 'add_staff.html',{'department_data':department_data,'staff_role':staff_role})

@never_cache
@login_required
def view_staff(request):
    staff_data = Staff.objects.all()
    return render(request, 'view_staff.html',{'staffdata':staff_data})


@login_required
@never_cache
def edit_staff(request, uid):
    
    data= Staff.objects.get(id=uid)
    department = Department.objects.all()
    
    return render(request, 'edit_staff.html',{"data":data, 'department':department})


@login_required
@never_cache
def update_staff(request, uid):
    if request.method == 'POST':
        value= Staff.objects.get(id=uid)
        form = TeacherData(request.POST, request.FILES, instance=value)
        if form.is_valid():
            form.save()
            return redirect(view_staff)
        return HttpResponse("Not Valid")
    return HttpResponse('No Data')


@login_required
@never_cache
def delete_staff(request, did):
    staff_to_delete = Staff.objects.get(id=did)
    staff_user = staff_to_delete.staff_id   
    staff_to_delete.delete()
    staff_user.delete()
    return redirect(view_staff)


# Staff Role Related


@login_required
@never_cache
def add_staff_role(request):
    if request.method=='POST':
        role=request.POST['role']
        staff_role=StaffRole.objects.create(role=role)
        staff_role.save()
        messages.warning(request,'Role is Added Successfully!')
        return redirect(view_staff)    
    return render(request, 'add_staff_role.html')



# staff attendance

@login_required
@never_cache
def mark_staff_attendance(request):
    if request.method == 'POST':
        staff_ids = request.POST.getlist('staff_ids')
        today = date.today()
        
        for staff_id in staff_ids:
            staff = Staff.objects.get(id=staff_id)
            status = request.POST.get(f'status_{staff_id}')
            notes = request.POST.get(f'notes_{staff_id}', '')
            
            # Check if attendance already exists for today
            attendance, created = StaffAttendance.objects.get_or_create(
                staff=staff,
                date=today,
                defaults={
                    'status': status,
                    'notes': notes
                }
            )
            
            if not created:
                attendance.status = status
                attendance.notes = notes
                attendance.save()
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('view_staff_attendance')
    
    else:
        staff_list = Staff.objects.all()
        today = date.today()
        return render(request, 'mark_staff_attendance.html', {
            'staff': staff_list,
            'today': today
        })

@login_required
@never_cache
def view_staff_attendance(request):
    attendance_list = StaffAttendance.objects.all().order_by('-date')
    return render(request, 'view_staff_attendance.html', {
        'attendance_list': attendance_list
    })


#Library

@admin_required
@login_required
@never_cache
def add_library_catogery(request):
    if request.method == 'POST':
        category_name=request.POST['category_name']
        category=LibraryBookCategory.objects.create(category_name=category_name)
        category.save()
        return HttpResponse("<script>window.alert('Library Catogery Added Successfully!'); window.location.href='view_library_category'</script>")
    else:
        
        return render(request, 'library_book_catogery.html')

def view_library_category(request):
    library_catogery=LibraryBookCategory.objects.all()
    return render(request, 'view_library_book_catogery.html',{'library_catogery':library_catogery})

def edit_book_category(request,cid):
    pass

def delete_book_category(request,cid):
    pass


def add_library_book(request):
    if request.method=='POST':
        book_data=LibraryData(request.POST,request.FILES)
        if book_data.is_valid():
            print("..............",book_data)
            book_data.save()
            return HttpResponse("Success")
        return HttpResponse("Error")
    
    else:
        books=LibraryData()
        
        return render(request, 'add_library_book.html',{'books':books})
    
def view_library_book(request):
    books=Book.objects.all()
    return render(request, 'view_library_book.html',{'books':books})





def about(request):
    return render(request, 'about.html')

def courses(request):
    return render(request, 'courses.html')

def trainers(request):
    return render(request, 'trainers.html')

def events(request):
    return render(request, 'events.html')

def pricing(request):
    return render(request, 'pricing.html')