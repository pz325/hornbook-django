# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import sys

# Create your models here.
class UserVocabulary(models.Model):
    user = models.ForeignKey(User, editable=False)
    vocabulary = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True, editable=False)

    # def __unicode__(self):
        # return '{0}: {1}'.format(self.user.username, self.vocabulary.encode(sys.stdout.encoding))
