# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from models import StudyHistory
import datetime
import json

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
    today = datetime.date.today()
    # update today's study history
    tomorrow = today + datetime.timedelta(days=1)
    StudyHistory.objects.filter(user=request.user, 
        study_date__range=(today, tomorrow)).delete()
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
