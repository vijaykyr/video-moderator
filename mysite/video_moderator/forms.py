from django import forms


class LocalSubmissionForm(forms.Form):
  upload = forms.FileField(label='Local File')
  api_key = forms.CharField(label='API Key', max_length=200)
  sample_rate = forms.IntegerField(label='Sample Rate', initial=1, min_value=1, max_value=120)
  response_type = forms.ChoiceField((
    ('perf', 'Performance Metrics'),
    ('api', 'Frame Annotations')
    ), required=False)

class GCSSubmissionForm(forms.Form):
  gcs_uri = forms.RegexField(label='GCS File', regex='gs://.*mp4')
  api_key = forms.CharField(label='API Key', max_length=200)
  sample_rate = forms.IntegerField(label='Sample Rate', initial=1, min_value=1, max_value=120)
  response_type = forms.ChoiceField((
    ('perf', 'Performance Metrics'),
    ('api', 'Frame Annotations')
    ), required=False)


