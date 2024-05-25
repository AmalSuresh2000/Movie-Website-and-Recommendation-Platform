from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from movie_app.models import Movie, Review

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(help_text="")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(help_text="Required. 50 characters or fewer. Letters only.")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 10:
            raise forms.ValidationError("Username must be 10 characters or fewer.")
        return username

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']
