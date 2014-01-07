# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist

from models import StudyHistory
import datetime
import json
import random

@login_required
def index(request):
    return render_to_response('study/index.html', 
        context_instance=RequestContext(request))

@login_required
def api_index(request):
    return render_to_response('study/api.html',
        context_instance=RequestContext(request))

@login_required
def new_study(request):
    '''
    HTTP POST /study/new_study
    Data
        vocabularies e.g. "u0x2345 u0x1111 u0x1111u0x1234"
    Return
        [<StudyHistory object>, <StudyHistory object>]
    '''
    vocabularies = request.POST['vocabularies'].split(' ')
    study_date = datetime.datetime.now()
    ret = []
    if vocabularies == '':
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))
    # add new StudyHistory
    for v in vocabularies:
        if v == '':
            continue
        try:
            study_history = StudyHistory.objects.get(user=request.user, vocabulary=v)
            study_history.study_date = study_date
            study_history.studied_times += 1
            study_history.revise_date = study_date
            study_history.history_type = 'N'
            study_history.save()
        except ObjectDoesNotExist:
            study_history = StudyHistory(user=request.user, vocabulary=v, study_date=study_date, revise_date=study_date, history_type='N', studied_times=0)
            study_history.save()
        
        ret.append(study_history.getJSONObject())

    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))

@login_required
def revise_study(request):
    '''
    HTTP POST /study/revise_study
    Data
        vocabularies e.g. "u0x2345 u0x1111 u0x1111u0x1234"
    Return
        [<StudyHistory object>, <StudyHistory object>]
    '''
    vocabularies = request.POST['vocabularies'].split(' ')
    revise_date = datetime.datetime.now()
    ret = []
    if vocabularies == '':
        return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))
    # update StudyHistory
    for v in vocabularies:
        if v == '':
            continue
        try:
            study_history = StudyHistory.objects.get(user=request.user, vocabulary=v)
            study_history.revise_date = revise_date
            study_history.history_type = get_history_type(study_history.study_date, study_history.revise_date)
            study_history.save()
            ret.append(study_history.getJSONObject())
        except ObjectDoesNotExist:
            continue

    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))


@login_required
def get_study_between(request):
    '''
    HTTP GET /study/get_study_between?start_date&end_date
    Return [u0x2345, u0x1111, ...]
    '''
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y').date()
    end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y').date() + datetime.timedelta(days=1)
    q = StudyHistory.objects.filter(user=request.user, 
        study_date__range=(start_date, end_date))
    ret = [h.vocabulary for h in q]
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))


@login_required
def get_all(request):
    '''
    HTTP GET /study/get_all
    Return [u0x2345, u0x1111, ...]
    '''
    ret = [h.vocabulary for h in StudyHistory.objects.all()]
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))


@login_required
def get_study_intelligent(request):
    '''
    HTTP GET /study/get_study_intelligent
    return study history intelligently:
     * return all New
     * return all Studying
     * return random 10 Grasped
    Return [u0x2345, u0x1111, ...]
    '''
    new_v = [h.vocabulary for h in StudyHistory.objects.filter(user=request.user, history_type='N')]
    studying_v = [h.vocabulary for h in StudyHistory.objects.filter(user=request.user, history_type='S')]
    grasped_v = [h.vocabulary for h in StudyHistory.objects.filter(user=request.user, history_type='G')]
    random.shuffle(grasped_v)

    ret = new_v + studying_v + grasped_v[:10];

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
