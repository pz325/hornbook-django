# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class UserVocabularyRecord(models.Model):
    user = models.ForeignKey(User, editable=False)
    date_stamp = models.DateTimeField(auto_now=False)
    num_new_vocabulary = models.PositiveSmallIntegerField(default=0)
    num_learning_vocabulary = models.PositiveSmallIntegerField(default=0)
    num_grasped_vocabulary = models.PositiveSmallIntegerField(default=0)

admin.site.register(UserVocabularyRecord)
