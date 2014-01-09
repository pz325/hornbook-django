#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist

import datetime
import json

from django.contrib.auth.models import User
from models import UserVocabularyRecord
from apps.study.models import StudyHistory

@login_required
def index(request):
    statistics = get_statistics_(request.user)
    return render(request, 
        'dashboard/index.html', 
        {"statistics": statistics})

@login_required
def get_statistics(request):
    '''
    HTTP GET /study/get_statistics
    Return
        {
            num_new: 3,
            num_studying: 4,
            num_grasped: 5
        }
    '''
    ret = get_statistics_(request.user)
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))

def get_statistics_(user):
    new_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='N')]
    studying_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='S')]
    grasped_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='G')]
    ret = dict(num_new=len(new_v),
        num_studying=len(studying_v),
        num_grasped=len(grasped_v))
    return ret

def update_record(user, num_new, num_studying, num_grasped):
    '''
    '''
    today = datetime.date.today()  # record uses date stamp
    try:
        r = UserVocabularyRecord.objects.get(user=user, date_stamp=today)
        r.num_new = num_new
        r.num_studying = num_studying
        r.num_grasped = r.num_grasped
        r.save()
    except ObjectDoesNotExist:
        r = UserVocabularyRecord(user=user, date_stamp=today, num_new=num_new, num_studying=num_studying, num_grasped=num_grasped)
        r.save()
    return r.getJSONObject()
