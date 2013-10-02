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
        vocabularies e.g. "u0x2345 u0x1111"
    Return
        {
            user: "xinrong",
            vocabularies: "u0x2345 u0x1111",
            study_date = "2013-10-02"
        }
    '''
    vocabularies = request.POST['vocabularies'].split(' ')
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    StudyHistory.objects.filter(user=request.user, 
        study_date__range=(today, tomorrow)).delete()
    for v in vocabularies:
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
    Return 
        {
            start_date: 2013-10-02,
            end_date: 2013-10-03,
            study_history: [{u_char: u0x2345}, {u_char: u0x1111}]
        }
    '''
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y').date()
    end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y').date() + datetime.timedelta(days=1)
    ret = dict(
        start_date = start_date,
        end_date = end_date,
        study_history = []
        )
    q = StudyHistory.objects.filter(user=request.user, 
        study_date__range=(start_date, end_date))
    for h in q:
        ret['study_history'].append(dict(u_char=h.vocabulary))
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))
