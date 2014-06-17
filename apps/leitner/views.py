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

from models import Leitner
from models import SessionCount


@login_required
def add(request):
    '''
    HTTP POST /leitner/add
    Data
        hanzi e.g. "u0x2345 u0x1111"
    '''
    hanziList = request.POST['hanzi'].split(' ')
    today = datetime.datetime.now()
    if hanziList == '':
        return
    for hanzi in hanziList:
        if hanzi == '':
            continue
        try:
            h = Leitner.objects.get(user=request.user, hanzi=hanzi)
            h.last_study_date = today
            h.forget_times += 1
            h.deck = 'C'   # Deck Current
            h.level = 0    # Level 1
            h.save()
        except ObjectDoesNotExist:
            h = Leitner(user=request.user, hanzi=hanzi, last_study_date=today)
            h.save()
    return

@login_required
def get(request):
    '''
    HTTP GET /leitner/get
    Return [u0x2345, u0x1111, ...]
    '''
    session_count = SessionCount.objects.get(user=request.user)
    session_deck_id = session_count['count'] % 10;

    current_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck='C')]
    level1_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck=str(session_deck_id), level=2)]
    level2_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck=str((session_deck_id-2)%10), level=3)]
    level3_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck=str((session_deck_id-5)%10), level=4)]
    level4_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck=str((session_deck_id+1)%10), level=4)]
    ret = current_deck + level1_deck + level2_deck + level3_deck + level4_deck
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))

@login_required
def count(request):
    '''
    HTTP GET /leitner/count?level
    Return 25
    '''
    level = int(request.GET['level'])
    count = Leitner.objects.filter(user=request.user, level=level).count()
    return HttpResponse(json.dumps(count, cls=DjangoJSONEncoder))

@login_required
def update(request):
    '''
    HTTP POST /Leitner/update
    Data
        recall_results: 
            a JSON array
            [
                {'hanzi': u0x2345, 'result': true},
                {'hanzi': u0x1111, 'result': false},
                ...
            ]
    '''
    recall_results = json.loads(request.POST['recall_results'])
    session_count = SessionCount.objects.get(user=request.user)
    session_deck_id = str(session_count['count'] % 10);
    today = datetime.datetime.now()

    for result in recall_results:
        try:
            h = Leitner.objects.get(user=request.user, hanzi=result['hanzi'])
            h.last_study_date = today
            if result['result'] == 'true':
                # move from Deck Current to Session Deck
                if h.deck == 'C': h.deck = session_deck_id
                # update level
                h.level += 1
                # move from Session Deck to Deck Retired
                if h.level == 5: h.deck = 'R'
            else:
                # move to Deck Current, set level to 0
                h.deck = 'C'
                h.level = 0
                h.forget_times += 1
            h.save()
        except ObjectDoesNotExist:
            pass
    
    # update session count
    session_count['count'] += 1
    session_count['timestamp'] = today
    session_count.save()
    return


from apps.study.models import StudyHistory
def importFromStudyHistory():
    for h in StudyHistory.objects.all():
        q = Leitner.objects.filter(hanzi=h.vocabulary)
        if not q:
            if h.history_type == 'N':
                # Deck Current, Level 0
                l = Leitner(user=h.user, hanzi=h.vocabulary, last_study_date=h.revise_date, forget_times=h.studied_times, deck='C', level='0')
                l.save()
            elif h.history_type == 'S':
                # Deck session (0), Level 1
                l = Leitner(user=h.user, hanzi=h.vocabulary, last_study_date=h.revise_date, forget_times=h.studied_times, deck='0', level='1')
                l.save()
            elif h.history_type == 'G':
                # Deck Retired, Level 5 
                l = Leitner(user=h.user, hanzi=h.vocabulary, last_study_date=h.revise_date, forget_times=h.studied_times, deck='R', level='5')
                l.save()
            else:
                raise Exception('Unknown history_type')