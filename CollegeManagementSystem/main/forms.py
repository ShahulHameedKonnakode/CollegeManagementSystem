from main.models import Student, Staff, Department, Book
from django import forms

class DepartmentData(forms.ModelForm):
    class Meta:
        model=Department
        fields = "__all__"

class StudentData(forms.ModelForm):
    class Meta:
        model=Student
        fields = "__all__"


class TeacherData(forms.ModelForm):
    
    class Meta:
        model=Staff
        fields = "__all__"

class LibraryData(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    


