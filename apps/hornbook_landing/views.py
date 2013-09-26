# Create your views here.
from django.shortcuts import render_to_response
import logging
from django.template import RequestContext
logger = logging.getLogger(__name__)

def index(request):
    return render_to_response('hornbook_landing/index.html', 
        context_instance=RequestContext(request))
    # if request.user.is_authenticated():
    #     logger.error('user is authenticated')
    #     return render_to_response('logged_in.html')
    # else:
    #     logger.error('user is not authenticated')
    #     return render_to_response('not_logged_in.html')
