from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Story
from .models import Comments


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Nationality', 'birth_date','image')
class StoryUpdate(forms.ModelForm):
    class Meta:
        model = Story
        fields =['title','resume','genres','langues','image']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['text']