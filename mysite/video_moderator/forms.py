from django import forms

#Todo:
# 1) Add validation that gcs uri is in format "gs://<bucket-name>/<file-path>"

class SubmissionForm(forms.Form):
  gcs_uri = forms.CharField(label='GCS URI', max_length=200)
  api_key = forms.CharField(label='API Key', max_length=200)
  sample_rate = forms.IntegerField(label='Sample Rate', max_value=120)

  def clean(self):
    cleaned_data = super(SubmissionForm, self).clean()
    cc_myself = cleaned_data.get("cc_myself")
    subject = cleaned_data.get("subject")

    if cc_myself and subject:
      # Only do something if both fields are valid so far.
      if "help" not in subject:
          raise forms.ValidationError(
              "Did not send for 'help' in the subject despite "
              "CC'ing yourself."
          )
