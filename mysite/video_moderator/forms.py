from django import forms

#Todo:
# 1) Add validation that gcs uri is in format "gs://<bucket-name>/<file-path>"

class SubmissionForm(forms.Form):
  upload = forms.FileField(label='', required=False)
  gcs_uri = forms.RegexField(label='GCS URI', regex='gs://.*mp4', required=False)
  api_key = forms.CharField(label='API Key', max_length=200)
  sample_rate = forms.IntegerField(label='Sample Rate', min_value=1, max_value=120)

  def clean(self):
    cleaned_data = super(SubmissionForm, self).clean()

