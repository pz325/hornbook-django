# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from rest_framework import serializers, viewsets

STUDY_HISTORY_TYPE = (
    ('N', 'New'),
    ('S', 'Studying'),
    ('G', 'Grasped'),
    )

# Create your models here.
class StudyHistory(models.Model):
    user = models.ForeignKey(User, editable=False)
    vocabulary = models.CharField(max_length=200)
    study_date = models.DateTimeField()
    revise_date = models.DateTimeField()
    history_type = models.CharField(max_length=1, choices=STUDY_HISTORY_TYPE)
    studied_times = models.PositiveSmallIntegerField(default=0)

    def getJSONObject(self):
        return dict(user=self.user.username,
            vocabulary=self.vocabulary,
            study_date=self.study_date,
            revise_date=self.revise_date,
            history_type=self.history_type,
            studied_times=self.studied_times)

class Reading(models.Model):
    # user = models.ForeignKey(User)
    article = models.CharField(max_length=500)
    book = models.CharField(max_length=500)
    study_date = models.DateTimeField()
    revise_date = models.DateTimeField()
    times = models.PositiveSmallIntegerField(default=0)

class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reading
        fileds = ('article', 'book', 'study_date', 'revise_date', 'times')

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer

class Recitation(models.Model):
    # user = models.ForeignKey(User)
    article = models.CharField(max_length=500)
    study_date = models.DateTimeField()
    revise_date = models.DateTimeField()
    times = models.PositiveSmallIntegerField(default=0)

class RecitationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recitation
        fileds = ('article', 'study_date', 'revise_date', 'times')

class RecitationViewSet(viewsets.ModelViewSet):
    queryset = Recitation.objects.all()
    serializer_class = RecitationSerializer

admin.site.register(StudyHistory)
admin.site.register(Reading)
admin.site.register(Recitation)
