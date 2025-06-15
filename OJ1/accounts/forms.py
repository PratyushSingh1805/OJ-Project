# from django import forms
# from .models import UserProfile

# class ProfilePicForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['profile_pic']

from django import forms
from .models import UserProfile
from .widgets import CustomClearableFileInput  # 
class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
        widgets = {
            'profile_pic': CustomClearableFileInput(attrs={'class': 'form-control'})
        }
        # widgets = {
        #     'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}, template_name='widgets/custom_file_input.html')
        # }
        # widgets = {
        #     'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set custom widget template
        self.fields['profile_pic'].widget.template_name = 'widgets/custom_file_input.html'
