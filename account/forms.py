from django import forms
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper

from .models import UserBase, Profile, Review


class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserBase
        fields = ['username', 'email', 'first_name', 'last_name','password1', 'password2']
        help_texts = {'email': "IMPORTANT: this field can NOT be changed!"}

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username and UserBase.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'mt-3'
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean(self, **kwargs):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        
        if (username and UserBase.objects.filter(username__iexact=username).exists()) and (UserBase.objects.get(username=username) != self.user):
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args,**kwargs)
        self.fields['email'].widget.attrs.update({'class':'mb-2','readonly':'readonly'})
        self.fields['username'].widget.attrs.update({'class':'mb-2'})
        self.fields['first_name'].widget.attrs.update({'class':'mb-2'})
        self.fields['last_name'].widget.attrs.update({'class':'mb-2'})

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'interests', 'image']
        help_texts = {'interests': "Hold down “Control”, or “Command” on a Mac, to select more than one."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['about'].widget.attrs.update({'class':'mb-2'})
        self.fields['image'].widget.attrs.update({'class':'mb-2'})

        self.helper = FormHelper()
        self.helper.label_class = 'mt-3'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['opinion', 'rate']



