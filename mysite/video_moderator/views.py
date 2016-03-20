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
            # process the data in form.cleaned_data
            moderate_results = moderate(form.cleaned_data.get('gcs_uri'),form.cleaned_data.get('sample_rate'),
                     form.cleaned_data.get('api_key'))
            return HttpResponse(moderate_results)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmissionForm()

    return render(request, 'video_moderator/submit_vid.html', {'form': form})