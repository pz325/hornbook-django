#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json

@login_required
def index(request):
    return render_to_response('dashboard/index.html', 
        context_instance=RequestContext(request))
