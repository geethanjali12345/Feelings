from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Notes,UserProfile

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class NotesForm(forms.ModelForm):
	class Meta:
		model=Notes
		exclude = ('user','slug','publish','favorite')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['first_name','last_name','profilepic', 'birthday','hobby', 'bio'
                 ]

    def save(self, user=None):
        user_profile = super(UserProfileForm,self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile