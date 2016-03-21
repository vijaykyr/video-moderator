from django.shortcuts import render
from django.http import HttpResponse

from .forms import LocalSubmissionForm
from .forms import GCSSubmissionForm

from vid_moderator import moderate


# Create your views here.
def submit_vid(request):
    if request.method == 'POST':
        if 'upload' in request.POST or 'upload' in request.FILES: #Local Submission
            form = LocalSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                return HttpResponse(moderate(request.FILES.get('upload'),form.cleaned_data.get('sample_rate'),
                                                 form.cleaned_data.get('api_key')))
            else:
                return render(request, 'video_moderator/submit_vid.html', {'local_form': form,
                                                                   'gcs_form': GCSSubmissionForm()})
        elif 'gcs_uri' in request.POST: #GCS Submission
            form = GCSSubmissionForm(request.POST)
            if form.is_valid():
                return HttpResponse(moderate(form.cleaned_data.get('gcs_uri'),form.cleaned_data.get('sample_rate'),
                                             form.cleaned_data.get('api_key')))
            else:
                return render(request, 'video_moderator/submit_vid.html', {'local_form': LocalSubmissionForm(),
                                                                   'gcs_form': form})
    elif request.method == 'GET': #render new form
        return render(request, 'video_moderator/submit_vid.html', {'local_form': LocalSubmissionForm(),
                                                                   'gcs_form': GCSSubmissionForm()})