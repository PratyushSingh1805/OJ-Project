from django import forms
from .models import Submission

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['language', 'code']

# from django import forms
# from .models import Submission

# class CodeSubmissionForm(forms.ModelForm):
#     LANGUAGE_CHOICES = [
#         ('py', 'Python'),
#         ('cpp', 'C++'),
#     ]

#     language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

#     class Meta:
#         model = Submission
#         fields = ['language', 'code']
