from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator


# Create your models here.

class User(AbstractUser):
    user_type = models.CharField(max_length=50)


class Department(models.Model):    
    dep_name=models.CharField(max_length=255)

    def __str__(self):
        return self.dep_name
    
class Sessions(models.Model) :
    session_name=models.CharField(max_length=100)
       
class Course(models.Model):
    course_code=models.CharField(max_length=100)
    course_name=models.CharField(max_length=255)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name
    
class Subject(models.Model):
    subject_code=models.CharField(max_length=100)
    subject_name=models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subject_name
    

class Student(models.Model): 
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)   
    mob = models.IntegerField()    
    photo = models.ImageField(upload_to='media/students_image')


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
        ('late', 'Late')

    ])
    notes = models.TextField(blank=True, null=True)



    # def __str__(self):
    #     return self.name

class StaffRole(models.Model):
    role=models.CharField(max_length=100)

class Staff(models.Model):  
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)  
    department_id=models.ForeignKey(Department, on_delete=models.CASCADE)
    role=models.ForeignKey(StaffRole,on_delete=models.CASCADE, null=True)
    mob = models.IntegerField()
    photo = models. ImageField(upload_to='media/staff_image')
    qualification = models. CharField(max_length=100)
    

    # def __str__(self):
    #     return self.name

class StaffAttendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
        ('late', 'Late')

    ])
    notes = models.TextField(blank=True, null=True)

class ExaminationGroup(models.Model):
    exam_group_name=models.CharField(max_length=255)   
    description=models.TextField(null=True) 
class Examination(models.Model):
    exam_group = models.ForeignKey(ExaminationGroup,null=True, on_delete=models.CASCADE)
    session=models.ForeignKey(Sessions, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=255)   
    description=models.TextField(null=True) 


class ExaminationSchedule(models.Model):
    exam_group=models.ForeignKey(ExaminationGroup, on_delete=models.CASCADE, null=True)
    exam_name=models.ForeignKey(Examination, on_delete=models.CASCADE )
    exam_subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date=models.DateField()
    exam_time=models.TimeField()
    room_no=models.CharField(max_length=30)
    min_mark=models.PositiveIntegerField()
    max_mark=models.PositiveIntegerField()

    


class Mark(models.Model):
    student_id=models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_schedule=models.ForeignKey(ExaminationSchedule, on_delete=models.CASCADE, null=True)
    mark = models.IntegerField()
    grade = models.CharField(max_length=30)




class LibraryBookCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.category_name


class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
    ]

    book_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    publication_date = models.DateField()
    category = models.ForeignKey('LibraryBookCategory', on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    edition = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    available_copies = models.PositiveIntegerField(default=0)
    rack_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if self.available_copies == 0:  # Explicit check for zero
            self.available_copies = self.quantity
        super().save(*args, **kwargs)