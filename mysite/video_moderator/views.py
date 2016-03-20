from django.shortcuts import render

# Create your views here.
def submit_vid(request):
    return render(request, 'video_moderator/submit_vid.html', {})