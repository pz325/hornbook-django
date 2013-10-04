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

def get_most_common_character(request):
    '''
    HTTP GET /api/most_common_character
    
    Resp: [{"u_char": "\u60c5"}]
    '''
    u_char = MostCommonCharacter.get_one()
    return_json = json.dumps([dict(u_char=u_char)])
    return HttpResponse(return_json)

def get_all_most_common_characters(request):
    '''
    HTTP GET /api/all_most_common_characters

    Resp: 
        [
            [{"u_char": "\u4e86"}], 
            [{"u_char": "\u662f"}], 
            ...
        ], sorted by frequency
    '''
    most_common_characters = MostCommonCharacter.get_all()
    most_common_characters = [[dict(u_char=ch)] for (ch, f) in most_common_characters]
    return_json = json.dumps(most_common_characters)
    return HttpResponse(return_json)

def get_most_common_word(request):
    '''
    HTTP GET /api/most_common_word?ref_character=一&last_word=一个

    Resp: [{"u_chars": "\u4e00"}, {"u_char": "\u4e5d"}, {"u_char": "\u516d"}] 
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
    ret = [dict(u_chars=ch) for ch in u_word]
    return_json = json.dumps(ret)
    return HttpResponse(return_json)
