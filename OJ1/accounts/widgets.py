from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_file_input.html'
