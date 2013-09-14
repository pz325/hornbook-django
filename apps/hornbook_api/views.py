#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse
from django.core.cache import cache
import os.path
import random
import json

def get_most_common_character(request):
    '''
    HTTP GET /api/most_common_character
    
    Resp: {"u_char": "\u60c5"}
    '''
    most_common_characters = cache.get('most_common_characters')
    if most_common_characters is None:
        f = open(os.path.dirname(__file__) + '/../../data/most_common_chinese_characters.txt')
        most_common_characters = f.readlines()
        cache.set('most_common_characters', most_common_characters)
    index = random.randint(0, len(most_common_characters)-1)
    u_char = unicode(most_common_characters[index], "utf-8").strip()
    return_json = json.dumps(dict(u_char=u_char))
    # self.response.headers['Content-Type'] = 'text/plain'
    # self.response.write(return_json)
    return HttpResponse(return_json)
