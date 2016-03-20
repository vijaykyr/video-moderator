from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SubmissionForm

# Create your views here.
def submit_vid(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmissionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'video_moderator/submit_vid.html', {'form': form})