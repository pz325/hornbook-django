# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from models import StudyHistory
from datetime import date
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
    Data vocabularies: "u0x2345 u0x1111"
    '''
    vocabularies = request.POST['vocabularies'].split(' ')
    today = date.today()
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
    Return [{u_char: u0x2345}, {u_char: u0x1111}]
    '''
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    # TODO: check date string mask
    q = StudyHistory.objects.filter(user=request.user, start_date__range=(start_date, end_date))
    ret = []
    for h in q:
        ret.append(dict(u_char=h['vocabulary']))
    return HttpResponse(json.dumps(ret))
