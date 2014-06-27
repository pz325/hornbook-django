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
from apps.leitner.models import Leitner


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
    num_new = Leitner.objects.filter(user=user, deck='C').count()
    num_study = Leitner.objects.filter(user=user, level__gt=0, level__lt=5).count()
    num_grasped = Leitner.objects.filter(user=user, level__gt=4).count()

    ret = dict(num_new=num_new,
        num_studying=num_study,
        num_grasped=num_grasped)
    return ret

from apps.hornbook_api.models import MostCommonCharacter

def get_most_common_statistics(user):
    v = [h.hanzi for h in Leitner.objects.filter(user=user)]
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
