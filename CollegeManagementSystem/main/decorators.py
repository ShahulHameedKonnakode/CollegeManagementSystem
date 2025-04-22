from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps


def admin_required(view_fucn):
    @wraps(view_fucn)

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_fucn(request, *args, **kwargs)
        return HttpResponse("Unauthorise access - Admin Only", status=403)
    return wrapper

def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'Teacher':
            return view_func(request, *args, **kwargs)
        return HttpResponse("Unauthorized Access - Teachers only", status=403)
    return wrapper

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'student':
            return view_func(request, *args, **kwargs)
        return HttpResponse("Unauthorized Access - Students only", status=403)
    return wrapper
