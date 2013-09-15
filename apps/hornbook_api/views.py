#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from models import MostCommonCharacter

from django.http import HttpResponse
import json


def get_most_common_character(request):
    '''
    HTTP GET /api/most_common_character
    
    Resp: {"u_char": "\u60c5"}
    '''
    u_char = MostCommonCharacter.get_one()
    return_json = json.dumps(dict(u_char=u_char))
    return HttpResponse(return_json)

def get_all_most_common_characters(request):
    '''
    HTTP GET /api/all_most_common_characters

    Resp: [{"frequency": 883634, "u_char": "\u4e86"}, {"frequency": 796991, "u_char": "\u662f"}, ...], sorted by frequency
    '''
    most_common_characters = MostCommonCharacter.get_all()
    most_common_characters = [dict(u_char=ch, frequency=f) for (ch, f) in most_common_characters]
    return_json = json.dumps(most_common_characters)
    return HttpResponse(return_json)
