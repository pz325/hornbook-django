# Create your views here.
from django.shortcuts import render_to_response
import logging

logger = logging.getLogger(__name__)

def index(request):
    if request.user.is_authenticated():
        logger.error('user is authenticated')
        return render_to_response('logged_in.html')
    else:
        logger.error('user is not authenticated')
        return render_to_response('not_logged_in.html')
