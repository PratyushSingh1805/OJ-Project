from django import forms
from .models import Submission

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['language', 'code']
