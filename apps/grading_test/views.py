# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

@login_required
def index(request):
    '''
    Test page for horn_api app
    '''
    return render_to_response('grading_test/index.html')