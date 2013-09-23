from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserVocabulary(models.Model):
    user = models.ForeignKey(User, editable=False)
    vocabulary = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True, editable=False)
