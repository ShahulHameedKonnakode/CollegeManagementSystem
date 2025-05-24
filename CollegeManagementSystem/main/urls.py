from django.urls import path
from main import views


urlpatterns = [

    path('export_attendance_pdf',views.export_attendance_pdf, name="export_attendance_pdf"),
    # login
    path('logins',views.logins, name='logins'),
    path('admin_home', views.admin_home, name="admin_home"),    
    path('logouts', views.logouts, name='logouts'),

    #admin
    path('admin_approve_students/<int:aid>',views.admin_approve_students, name='admin_approve_students'),

    # session
    path('add_session', views.add_session, name="add_session"),

    #department
    path('', views.index, name="index"),
    path('add_department', views.add_department, name='add_department'),
    path('view_department', views.view_department, name='view_department'),
    path('edit_department/<int:eid>', views.edit_department, name='edit_department'),
    path('update_department/<int:uid>', views.update_department, name='update_department'),
    path('delete_department/<int:did>', views.delete_department, name='delete_department'),  
    #course
    path('add_course',views.add_course, name='add_course'), 
    path('view_course',views.view_course, name='view_course'), 
    path('edit_course/<int:eid>',views.edit_course, name='edit_course'),
    path('delete_course/<int:did>', views.delete_course, name="delete_course"),

    #subject
    path('add_subject',views.add_subject, name="add_subject"),
    path('view_subject', views.view_subject, name="view_subject"),
    path('edit_subject/<int:eid>', views.edit_subject, name="edit_subject"),
    path('delete_subject/<int:did>',views.delete_subject, name="delete_subject"),

    #examination
    path('create_examination', views.create_examination, name='create_examination'),
    path('view_examination', views.view_examination, name='view_examination'),

    #examination schedule
    path('create_examination_group',views.create_examination_group, name='create_examination_group'),
    path('examination_schedule',views.create_examination_schedule, name='examination_schedule'),
    path('view_examination_schedule',views.view_examination_schedule, name='view_examination_schedule'),
    path('mark_entry',views.mark_entry, name='mark_entry'),
    path('result',views.result, name='result'),

    #student 
    path('add_student', views.add_student, name='add_student' ),
    path("view_std",views.view_std, name="view_std"),
    path("edit_std/<int:eid>", views.edit_std, name="edit_std"),
    path("update_std/<int:uid>", views.update_std, name="update_std"),
    path("delete_std/<int:did>", views.delete_std, name="delete_std"),

    
    #student_attendance
    path('mark_student_attendance', views.mark_student_attendance, name='mark_student_attendance'),
    path('view_student_attendance', views.view_student_attendance, name='view_student_attendance'),

    #staff
    path('add_staff/', views.add_staff, name='add_staff'),    
    path("view_staff",views.view_staff, name="view_staff"),
    path("edit_staff/<int:uid>",views.edit_staff, name="edit_staff"),
    path("update_staff/<int:uid>", views.update_staff, name='update_staff'),    
    path("delete_staff/<int:did>",views.delete_staff, name="delete_staff"),
    




    # staff_role
    path("add_staff_role", views.add_staff_role, name="add_staff_role"),

    #staff_attendance
    path('mark_staff_attendance', views.mark_staff_attendance, name='mark_staff_attendance'),
    path('view_staff_attendance', views.view_staff_attendance, name='view_staff_attendance'),


    # library
    path('add_library_catogery', views.add_library_catogery, name='add_library_catogery'),
    path('view_library_category', views.view_library_category, name='view_library_category'),
    path('add_library_book', views.add_library_book, name='add_library_book'),
    path('view_library_book', views.view_library_book, name='view_library_book'),
    

    

    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('trainers/', views.trainers, name='trainers'),
    path('events/', views.events, name='events'),
    path('pricing/', views.pricing, name='pricing'),
 

    

    

    
]