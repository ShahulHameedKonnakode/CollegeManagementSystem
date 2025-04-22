from django.urls import path
from student import views



app_name = 'student' 
urlpatterns = [
    path('student_home',views.student_home, name='student_home'),
    path("view_course_student",views.view_course_student, name="view_course_student"),
    path("view_student_attendance_student",views.view_student_attendance_student, name="view_student_attendance_student"),
    path("view_examination_schedule_student",views.view_examination_schedule_student, name="view_examination_schedule_student"),
    path('exam_registration', views.exam_registration, name='exam_registration'),
    path('get_exam_schedule/<int:eid>', views.get_exam_schedule, name='get_exam_schedule'),
    path("result_student",views.result_student, name="result_student"),
    path("view_library_book_student",views.view_library_book_student, name="view_library_book_student"),

    

]