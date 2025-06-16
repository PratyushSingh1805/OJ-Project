# from django import forms
# from .models import Problem, Tag

# class ProblemForm(forms.ModelForm):
#     class Meta:
#         model = Problem
#         fields = ['title', 'description']

from django import forms
from .models import Problem, Tag

class ProblemForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma-separated tags")

    class Meta:
        model = Problem
        fields = ['title', 'description', 'input_format', 'output_format',
                  'constraints', 'sample_input', 'sample_output', 'difficulty']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'input_format': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'output_format': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'constraints': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sample_input': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'sample_output': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing, populate tags
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Clear existing tags and add new ones
            instance.tags.clear()
            tag_names = [name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)
        return instance
