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
    Data  vocabulary: "u0x2345u0x1234"
    '''
    # import pdb; pdb.set_trace()
    vocabulary = request.POST["vocabulary"]

    q = UserVocabulary.objects.filter(user=request.user)
    q = q.filter(vocabulary=vocabulary)
    
    if q.count() == 0:
        v = UserVocabulary(user=request.user, vocabulary=vocabulary)
        v.save()
        ret = dict(user=request.user.username,
            vocabulary=vocabulary,
            status="added");
    else:
        ret = dict(user=request.user.username,
            vocabulary=vocabulary,
            status="not added");
    return HttpResponse(json.dumps(ret))
