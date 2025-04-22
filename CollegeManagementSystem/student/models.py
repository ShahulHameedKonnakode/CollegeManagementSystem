from django.db import models
from main.models import User,Examination,Subject,ExaminationGroup


# Create your models here.

class StudentExamRegistration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_group=models.ForeignKey(ExaminationGroup,on_delete=models.CASCADE, null=True)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    registration_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)