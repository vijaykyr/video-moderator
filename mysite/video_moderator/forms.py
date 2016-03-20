from django import forms

class SubmissionForm(forms.Form):
    gcs_uri = forms.CharField(label='GCS URI', max_length=200)
    api_key = forms.CharField(label='API Key', max_length=200)