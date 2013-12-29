# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
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
def save_study(request):
    '''
    HTTP POST /study/save_study
    Data 
        vocabularies e.g. "u0x2345 u0x1111 u0x1111u0x1234"
    Return
        {
            user: "xinrong",
            vocabularies: "u0x2345u0x1111",
            study_date = "2013-10-02"
        }
    '''
    vocabularies = request.POST['vocabularies'].split(' ')
    if vocabularies == '':
        return HttpResponse('nothing saved')
    today = datetime.datetime.now()
    # update today's study history
    for v in vocabularies:
        if v == '':
            continue
        learned = StudyHistory.objects.filter(vocabulary=v)
        if learned:
            learned.update(study_date=today)
        else:
            h = StudyHistory(user=request.user, vocabulary=v, study_date=today)
            h.save()

    ret = dict(user=request.user.username,
        vocabularies=vocabularies,
        study_date=today)
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
     * return all most recently studied, which then includes recapped
     * return random 10 within one week before the most recent study date
     * return random 10 within one month before the most recent study date 
    Return [u0x2345, u0x1111, ...]
    '''
    most_recent_study_date = StudyHistory.objects.filter(user=request.user).order_by("-study_date")[0].study_date
    one_day_before = most_recent_study_date - datetime.timedelta(days=1)
    most_recent = [h.vocabulary for h in StudyHistory.objects.filter(
        user=request.user,
        study_date__range=(
            one_day_before+datetime.timedelta(seconds=1), 
            most_recent_study_date))]

    one_week_before = most_recent_study_date - datetime.timedelta(days=7)
    one_week = [h.vocabulary for h in StudyHistory.objects.filter(
        user=request.user,
        study_date__range=(
            one_week_before+datetime.timedelta(seconds=1), 
            one_day_before))]
    random.shuffle(one_week)

    before = [h.vocabulary for h in StudyHistory.objects.filter(
        user=request.user,
        study_date__lt=one_week_before)]
    random.shuffle(before)

    ret = most_recent + one_week[:10] + before[:15]

    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))
