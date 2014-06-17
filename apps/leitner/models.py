# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class SessionCount(models.Model):
    user = models.ForeignKey(User, editable=False)
    count = models.PositiveSmallIntegerField(default=0)
    timestamp = models.DateTimeField()

LEITER_DECK_TYPE = (
    ('C', 'Current'),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('R', 'Retired'),
    )

LEITER_LEVEL = (
    (0, 'Level 0'),
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),
    (5, 'Level 5'),
    )

class Leitner(models.Model):
    '''
    Leitner system, a spaced repetition method. 
    refer to http://en.wikipedia.org/wiki/Leitner_system
    Here we implements the Example Two
    '''
    user = models.ForeignKey(User, editable=False)
    hanzi = models.CharField(max_length=10)
    deck = models.CharField(max_length=1, choices=LEITER_DECK_TYPE, default='C')
    level = models.PositiveSmallIntegerField(choices=LEITER_LEVEL, default=0)
    forget_times = models.PositiveSmallIntegerField(default=0)
    last_study_date = models.DateTimeField();

admin.site.register(Leitner)
admin.site.register(SessionCount)