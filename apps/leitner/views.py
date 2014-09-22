#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import datetime
import json
import logging
import random

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
    if hanziList == '':
        return
    for hanzi in hanziList:
        if hanzi == '':
            continue
        try:
            h = Leitner.objects.get(user=request.user, hanzi=hanzi)
            h.forget_times += 1
            h.deck = 'C'   # Deck Current
            h.level = 0    # Level 1
            h.save()
        except ObjectDoesNotExist:
            h = Leitner(user=request.user, hanzi=hanzi)
            h.save()
    return

@login_required
def get(request):
    '''
    HTTP GET /leitner/get
    Return [u0x2345, u0x1111, ...]
    '''
    numRetired = 5
    numPermanent = 10
    try:
        session_count = SessionCount.objects.get(user=request.user)
    except ObjectDoesNotExist:
        today = datetime.datetime.now()
        session_count = SessionCount(user=request.user, count=0, timestamp=today)
        session_count.save()
    deck_ids  = get_deck_ids(session_count)

    current_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck='C')]
    level1_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck=str(deck_ids[0]), level=1)]
    level2_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck=str(deck_ids[1]), level=2)]
    level3_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck=str(deck_ids[2]), level=3)]
    retired_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck='R')]
    permanent_deck = [h.hanzi for h in Leitner.objects.filter(user=request.user, deck='P')]

    # logging
    all_deck = Leitner.objects.filter(user=request.user)
    log_all(all_deck)

    random.shuffle(retired_deck)
    random.shuffle(permanent_deck)
    log_get_result(current_deck, level1_deck, level2_deck, level3_deck, retired_deck[:numRetired], permanent_deck[:numPermanent])
    ret = current_deck + level1_deck + level2_deck + level3_deck + retired_deck[:numRetired] + permanent_deck[:numPermanent]
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))


def get_deck_ids(session_count):
    '''
    @return session deck id for level 1, 2, and 3, respectively
    '''
    session_deck_id = session_count.count % 10
    level1_deck_id = (session_deck_id-2)%10
    level2_deck_id = (session_deck_id+5)%10
    level3_deck_id = (session_deck_id+1)%10
    log_str = '\nsession count: {session_count} -> session deck id: {session_deck_id}\n'.format(session_count=session_count.count, session_deck_id=session_deck_id)
    log_str += 'Level 1 deck: {deck_id}\n'.format(deck_id=level1_deck_id)
    log_str += 'Level 2 deck: {deck_id}\n'.format(deck_id=level2_deck_id)
    log_str += 'Level 3 deck: {deck_id}\n'.format(deck_id=level3_deck_id)
    logging.info(log_str)
    return (level1_deck_id, level2_deck_id, level3_deck_id)


def log_get_result(current_deck, level1_deck, level2_deck, level3_deck, retired_deck, permanent_deck):
    log_str = '\n/leitner/get result\n'
    log_str += '{n} from Current Deck {deck}\n'.format(n=len(current_deck), deck=current_deck)
    log_str += '{n} from Level 1 Deck {deck}\n'.format(n=len(level1_deck), deck=level1_deck)
    log_str += '{n} from Level 2 Deck {deck}\n'.format(n=len(level2_deck), deck=level2_deck)
    log_str += '{n} from Level 3 Deck {deck}\n'.format(n=len(level3_deck), deck=level3_deck)
    log_str += '{n} from Retired Deck {deck}\n'.format(n=len(retired_deck), deck=retired_deck)
    log_str += '{n} from Permanent Deck {deck}\n'.format(n=len(permanent_deck), deck=permanent_deck)
    logging.info(log_str)

def log_all(all_deck):
    decks = {'C': [], '1': {}, '2': {}, '3': {}, 'R': [], 'P': []}
    for j in range(1, 4):
        for i in range(0, 10):
            decks[str(j)][str(i)] = []
    for h in all_deck:
        if h.deck == 'C' or h.deck == 'R' or h.deck == 'P':
            decks[h.deck].append(h.hanzi)
        elif h.level == 1 or h.level == 2 or h.level == 3:
            decks[str(h.level)][h.deck].append(h.hanzi)
        else:
            logging.info('missing: {hanzi}'.format(hanzi=h.hanzi))
    log_str = 'ALL:\n'
    log_str += '{n} in Current Deck:\n'.format(n=len(decks['C']), deck_C=decks['C'])
    for j in range(1, 4):
        log_str += 'Level {j}:\n'.format(j=j)
        for i in range(0, 10):
            log_str += '    {n} in Deck {i}:\n'.format(n=len(decks[str(j)][str(i)]), i=i, deck_i=decks[str(j)][str(i)])
    log_str += '{n} in Retired Deck:\n'.format(n=len(decks['R']), deck_R=decks['R'])
    log_str += '{n} in Permanent Deck:\n'.format(n=len(decks['P']), deck_P=decks['P'])
    logging.info(log_str)
    


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
            a JSON object
            {
                "grasped": "u0x2345 u0x1111",
                "unknown": "u0x2345 u0x1111"
            }
    '''
    recall_results = json.loads(request.POST['recall_results'])
    session_count = SessionCount.objects.get(user=request.user)
    logging.info('sesson count {session_count}'.format(session_count=session_count.count))
    session_deck_id = str(session_count.count%10);

    grasped_recall = recall_results['grasped'].split(' ')
    for hanzi in grasped_recall:
        try:
            h = Leitner.objects.get(user=request.user, hanzi=hanzi)
            # update level
            h.level += 1
            # move from Deck Current to Session Deck
            if h.deck == 'C': h.deck = session_deck_id
            # move from Session Deck to Deck Retired
            if h.level == 4: h.deck = 'R'
            # move from Deck Retired to Deck Permanent
            if h.level >= 5:
                h.level = 5
                h.deck = 'P'
            log_hanzi(h, 'grasped')
            h.save()
        except ObjectDoesNotExist:
            logging.info('ObjectDoesNotExist')
            pass
        except MultipleObjectsReturned:
            logging.info('MultipleObjectsReturned')
            pass

    unknown_recall = recall_results['unknown'].split(' ')
    for hanzi in unknown_recall:
        try:
            h = Leitner.objects.get(user=request.user, hanzi=hanzi)
            # move to Deck Current, set level to 0
            h.deck = 'C'
            h.level = 0
            h.forget_times += 1
            log_hanzi(h, 'forget')
            h.save()
        except ObjectDoesNotExist:
            pass
    
    # update session count
    session_count.count += 1
    session_count.save()
    return

def log_hanzi(h, msg):
    logging.info(h.hanzi)
    logging.info('{msg}: deck: [{deck}] level: [{level}]'.format(msg=msg, deck=h.deck, level=h.level))


from apps.study.models import StudyHistory
def importFromStudyHistory():
    for h in StudyHistory.objects.all():
        q = Leitner.objects.filter(hanzi=h.vocabulary, user=h.user)
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
