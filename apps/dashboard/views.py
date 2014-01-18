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
import logging

from django.contrib.auth.models import User
from models import UserVocabularyRecord
from apps.study.models import StudyHistory

@login_required
def index(request):
    ret1 = get_study_history_statistics(request.user)
    ret2 = get_most_common_statistics(request.user)
    ret1.update(ret2)
    statistics = ret1
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
    ret = get_study_history_statistics(request.user)
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))

def get_study_history_statistics(user):
    new_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='N')]
    studying_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='S')]
    grasped_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='G')]
    ret = dict(num_new=len(new_v),
        num_studying=len(studying_v),
        num_grasped=len(grasped_v))
    return ret


from apps.hornbook_api.models import MostCommonCharacter

def get_most_common_statistics(user):
    v = []
    for h in StudyHistory.objects.filter(user=user):
        if len(h.vocabulary) > 1:
            for c in h.vocabulary:
                v.append(c)
        else:
            v.append(h.vocabulary)
    
    v = set(v)
    common = [c for (c, f) in MostCommonCharacter.get_all()]
    in_common = 0
    out_common = 0
    for h in v:
        if h in common:
            in_common += 1
        else:
            out_common += 1
    ret = dict(in_common=in_common, 
        out_common=out_common)
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
