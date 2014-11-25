# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist

from models import StudyHistory
from models import Reading
from models import Recitation

import datetime
import json
import random
import apps.leitner.views


import logging

@login_required
def index(request):
    return render_to_response('study/index.html', 
        context_instance=RequestContext(request))

@login_required
def learn_new(request):
    return render_to_response('study/new.html', 
        context_instance=RequestContext(request))

@login_required
def recap(request):
    return render_to_response('study/recap.html', 
        context_instance=RequestContext(request))

@login_required
def api_index(request):
    return render_to_response('study/api.html',
        context_instance=RequestContext(request))

@login_required
def save_new_study(request):
    '''
    HTTP POST /study/new_study
    Data
        vocabularies e.g. "u0x2345 u0x1111 u0x1111u0x1234"
    save to Leitner system
    '''
    apps.leitner.views.add(request)
    return HttpResponse()


@login_required
def update(request):
    '''
    HTTP POST /study/update
    Data
        recall_results: 
            a JSON object
            {
                "grasped": "u0x2345 u0x1111",
                "unknown": "u0x2345 u0x1111"
            }
    '''
    apps.leitner.views.update(request)
    return HttpResponse();

@login_required
def get_study_intelligent(request):
    '''
    HTTP GET /study/get_study_intelligent
    return study history intelligently, using Leitner service
    Return [u0x2345, u0x1111, ...]
    '''
    return apps.leitner.views.get(request)

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
    new_v = [h.vocabulary for h in StudyHistory.objects.filter(user=request.user, history_type='N')]
    studying_v = [h.vocabulary for h in StudyHistory.objects.filter(user=request.user, history_type='S')]
    grasped_v = [h.vocabulary for h in StudyHistory.objects.filter(user=request.user, history_type='G')]
    ret = dict(num_new=len(new_v),
        num_studying=len(studying_v),
        num_grasped=len(grasped_v))

    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))

from apps.hornbook_api.models import MostCommonCharacter
@login_required
def get_new_from_500(request):
    '''
    HTTP GET /study/get_new_from_500?num=3
    Return
        [u0x2345, u0x1111, ...]
    '''
    ret = []
    if 'num' in request.GET:
        num = int(request.GET['num'])   
    else:
        num = 3
    common500 = [ch for (ch, f) in MostCommonCharacter.get_all()]

    for v in StudyHistory.objects.filter(user=request.user):
        if v.vocabulary in common500:
            common500.remove(v.vocabulary)
    ret = common500[:num]

    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))


def get_history_type(study_date, revise_date):
    '''
    @return
        'N' study_date == revise_date
        'S' study_date < revise_date < study_date + 4
        'G' revise_date >= study_date + 4
    '''
    s = study_date.date()
    r = revise_date.date()
    delta = r - s
    if delta.days == 0:
        return 'N'
    if delta.days > 0 and delta.days < 4:
        return 'S'
    if delta.days >= 4:
        return 'G' 
    return 'N'

from apps.dashboard.views import update_record
def update_user_vocabulary_record(user):
    new_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='N')]
    studying_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='S')]
    grasped_v = [h.vocabulary for h in StudyHistory.objects.filter(user=user, history_type='G')]
    update_record(user, len(new_v), len(studying_v), len(grasped_v))
