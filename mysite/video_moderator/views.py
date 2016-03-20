from django.shortcuts import render
from django.http import HttpResponse

from .forms import SubmissionForm
from vid_moderator import moderate


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
            moderate(form.cleaned_data.get('gcs_uri'),5,form.cleaned_data.get('api_key'))
            return HttpResponse("return this string")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'video_moderator/submit_vid.html', {'form': form})