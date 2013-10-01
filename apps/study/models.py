# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import sys
from django.contrib import admin

# Create your models here.
class StudyHistory(models.Model):
    user = models.ForeignKey(User, editable=False)
    vocabulary = models.CharField(max_length=200)
    study_date = models.DateTimeField(auto_now=True) 

admin.site.register(StudyHistory)