# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

STUDY_HISTORY_TYPE = (
    ('N', 'New'),
    ('S', 'Studying'),
    ('G', 'Grasped'),
    )

# Create your models here.
class StudyHistory(models.Model):
    user = models.ForeignKey(User, editable=False)
    vocabulary = models.CharField(max_length=200)
    study_date = models.DateTimeField(auto_now=True)
    revise_date = models.DateTimeField(null=True)
    history_type = models.CharField(null=True, max_length=1, choices=STUDY_HISTORY_TYPE)
    studied_times = models.PositiveSmallIntegerField(default=0)

    def getJSONObject(self):
        return dict(user=self.user.username,
            vocabulary=self.vocabulary,
            study_date=self.study_date,
            revise_date=self.revise_date,
            history_type=self.history_type,
            studied_times=self.studied_times)

admin.site.register(StudyHistory)
