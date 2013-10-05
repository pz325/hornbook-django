# -*- coding: utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from models import UserVocabulary
from django.http import HttpResponse
import json
import logging

logger = logging.getLogger(__name__)

@login_required
def add_to_user_vocabulary(request):
    '''
    @login_required
    HTTP POST user_vocabularies/add_to_user_vocabulary
    Data  vocabulary: [{u_char: u0x2345}, {u_char: u0x1234}, ...]
    '''
    # import pdb; pdb.set_trace()
    logger.debug(request.body)
    vocabulary = simplejson.loads(request.body)
    logger.debug(vocabulary);
    # convert to unicode string: "u0x2345u0x1234"
    v_str = "";
    for ch in vocabulary:
        v_str += ch["u_char"]
    logger.debug(v_str)


    q = UserVocabulary.objects.filter(user=request.user)
    q = q.filter(vocabulary=v_str)
    
    if q.count() == 0:
        v = UserVocabulary(user=request.user, vocabulary=v_str)
        v.save()
        ret = dict(user=request.user.username,
            vocabulary=v_str,
            status="added");
        return HttpResponse(json.dumps(ret))
    else:
        ret = dict(user=request.user.username,
            vocabulary=v_str,
            status="not added");
        return HttpResponse(json.dumps(ret))
