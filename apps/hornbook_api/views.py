#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from models import MostCommonCharacter
from models import MostCommonWord
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import random

def index(request):
    '''
    Test page for horn_api app
    '''
    return render_to_response('hornbook_api/index.html')

def api_index(request):
    '''
    Test page for hornbook_api
    '''
    return render_to_response('hornbook_api/api.html')

def get_most_common_character(request):
    '''
    HTTP GET /api/most_common_character
    
    Resp: "\u60c5"
    '''
    u_char = MostCommonCharacter.get_one()
    return HttpResponse(u_char)

def get_all_most_common_characters(request):
    '''
    HTTP GET /api/all_most_common_characters

    Resp: ["\u4e86", "\u662f", ...], sorted by frenquency
    '''
    most_common_characters = MostCommonCharacter.get_all()
    most_common_characters = [ch for (ch, f) in most_common_characters]
    return_json = json.dumps(most_common_characters)
    return HttpResponse(return_json)

def get_most_common_word(request):
    '''
    HTTP GET /api/most_common_word?ref_character=一&last_word=一个

    Resp: "\u4e00\u4e5\u516d"
    '''
    ref_character = request.GET['ref_character']
    last_word = request.GET['last_word']

    word_candidates = MostCommonWord.get_words(ref_character)
    # logging.info('ref_character {0}'.format(list(ref_character)))
    # logging.info('last_word {0}'.format(list(last_word)))
    # for u_word in word_candidates:
        # logging.info('word_candidate {0}'.format(list(u_word)))
    while(True):
        index = random.randint(0, len(word_candidates)-1)
        u_word = word_candidates[index]
        if u_word != last_word:
            break
    return HttpResponse(u_word)


import hanzi_base
from models import Pinyin

def generateAllPinyin():
    for initial in hanzi_base.INITIAL:
        for final in hanzi_base.FINAL:
            for tone in hanzi_base.TONES:
                print initial, final, tone
                pinyin = Pinyin(
                    initial=initial, 
                    final=final, 
                    tone=tone)
                pinyin.save()