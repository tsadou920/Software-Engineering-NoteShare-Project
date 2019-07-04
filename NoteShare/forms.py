from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from cms.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('username', 'email', 'is_staff')