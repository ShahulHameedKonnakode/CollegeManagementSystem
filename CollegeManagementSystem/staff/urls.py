from django.urls import path
from staff import views



app_name = 'staff' 
urlpatterns = [


    path('teacher_home',views.teacher_home, name='teacher_home'),
    path("edit_staff_profile/<int:uid>",views.edit_staff_profile, name="edit_staff_profile"),

    # staff logging accessable pages
    path("view_std_staff",views.view_std_staff, name="view_std_staff"),
    path("view_staff_staff",views.view_staff_staff, name="view_staff_staff"),
    path("view_course_staff",views.view_course_staff, name="view_course_staff"),
    path("view_subject_staff",views.view_subject_staff, name="view_subject_staff"),
    path("mark_student_attendance_staff",views.mark_student_attendance_staff, name="mark_student_attendance_staff"),
    path("view_student_attendance_staff",views.view_student_attendance_staff, name="view_student_attendance_staff"),
    path("view_staff_attendance_staff",views.view_staff_attendance_staff, name="view_staff_attendance_staff"),
    path("view_examination_schedule_staff",views.view_examination_schedule_staff, name="view_examination_schedule_staff"),
    path("mark_entry_staff",views.mark_entry_staff, name="mark_entry_staff"),
    path("result_staff",views.result_staff, name="result_staff"),
    path("view_library_book_staff",views.view_library_book_staff, name="view_library_book_staff"),
    
]