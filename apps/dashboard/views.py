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

from django.contrib.auth.models import User
from models import UserVocabularyRecord
from apps.study.models import StudyHistory

@login_required
def index(request):
    return render_to_response('dashboard/index.html', 
        context_instance=RequestContext(request))

@login_required
def get_user_vocabulary_record(request):
    '''
    HTTP GET /dashboard/get_user_vocabular_record?date_from&date_to&period

    Get user's vocabulary record, from date_from to date_to
    
    @param date_from string of datetime, in the format of %m/%d/%Y
    @param date_to string of datetime, in the format of %m/%d/%Y
    @param period enum {last_week, last_month_, last_3_month, last_half_year, last_year, all}
    @return JSON string
        {
            'start': date_from,
            'end': date_to,
            'period': period,
            'data': [             // a list of results
                {
                    'date_stamp': date_stamp,
                    'num_new_vocabulary': num_new_vocabulary,
                    'num_learning_vocabulary': num_learning_vocabulary,
                    'num_grasped_vocabulary': num_grasped_vocabulary
                },
                {
                    ...
                }
            ]
        }
    '''
    return HttpResponse(json.dumps(ret, cls=DjangoJSONEncoder))

def get_user_vocabulary_record_(user, date_from, date_to):
    '''
    Get user's vocabulary records from date_from to date_to (record on date_to is included)
    
    @param user type of django.contrib.auth.models.User
    @param date_from type of datetime.datetime
    @param date_to type of datetime.datetime
    @return list of UserVocabularyRecord instances
    '''
    pass

def update_user_vocabulary_record(user, date_from):
    '''
    Update user's vocabulary record since date_from

    @param user type of django.contrib.auth.models.User
    @param date_from type of datetime.datetime
    '''
    pass
