# Create your views here.
from django.contrib.auth.decorators import login_required
from models import UserVocabulary
from django.http import HttpResponse

@login_required
def add_to_user_vocabulary(request):
    '''
    @login_required
    HTTP POST user_vocabularies/add_to_user_vocabulary
    Data  vocabulary: u0x2345
    '''
    vocabulary = request.POST['vocabulary']
    user_vocabulary = UserVocabulary(user=request.user, vocabulary=vocabulary)
    user_vocabulary.save()

    return HttpResponse("saved")
