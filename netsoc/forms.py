from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import PasswordChangeForm

class UserForm(forms.Form):
    '''Registration form for a new user'''
    first_name=forms.CharField(label='First Name', min_length=2 , max_length = 20)
    last_name=forms.CharField(label='Last Name', min_length=2 , max_length =20)
    gender_choices=(('M','Male'),('F','Female'),('O','Other'))
    gender=forms.ChoiceField(label='Gender', required=True , widget=forms.RadioSelect,choices=gender_choices)
    dob=forms.DateField(label='Date Of Birth',widget=forms.SelectDateWidget(years=[y for y in range(1930,2005)]))
    username= forms.CharField(label='Enter Username' , min_length=4 , max_length = 50)
    email = forms.EmailField(label= 'Enter your email id')
    password=forms.CharField(label='Enter Password', min_length =8, widget = forms.PasswordInput)

class PostForm(forms.ModelForm):

    class Meta:
        model=models.post
        fields=['post_text']

class CommentForm(forms.ModelForm):

    class Meta:
        model=models.comment
        fields=['comment_text']

class ProfileForm(forms.Form):
    '''Form to edit profile details of a user'''
    first_name=forms.CharField(label='First Name', min_length=2 , max_length = 20)
    last_name=forms.CharField(label='Last Name', min_length=2 , max_length =20)
    gender_choices=(('M','Male'),('F','Female'),('O','Other'))
    gender=forms.ChoiceField(label='Gender', required=True , widget=forms.RadioSelect,choices=gender_choices)
    dob=forms.DateField(label='Date Of Birth',widget=forms.SelectDateWidget(years=[y for y in range(1930,2005)]))
    username= forms.CharField(label='Enter Username' , min_length=4 , max_length = 50)
    email = forms.EmailField(label= 'Enter your email id')

class DescriptionForm(forms.Form):

    description=forms.CharField(label='Describe Yourself' , required=False , max_length =200)

class ImageForm(forms.Form):

    image=forms.ImageField()
