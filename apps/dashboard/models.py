# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class UserVocabularyRecord(models.Model):
    user = models.ForeignKey(User, editable=False)
    date_stamp = models.DateTimeField(auto_now=False)
    num_new = models.PositiveSmallIntegerField(default=0)
    num_studying = models.PositiveSmallIntegerField(default=0)
    num_grasped = models.PositiveSmallIntegerField(default=0)

    def getJSONObject(self):
        return dict(user=self.user.username,
            date_stamp=self.date_stamp,
            num_new=self.num_new,
            num_studying=self.num_studying,
            num_grasped=self.num_grasped)

admin.site.register(UserVocabularyRecord)
