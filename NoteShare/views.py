from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from cms.models import CustomUser #watch out for error

# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect

class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    # success_url = HttpResponseRedirect('')
    # success_url = redirect('')
    template_name = 'register.html'

def getAllUsernames():
	allUsers = CustomUser.objects.all()
	users = []
	for user in allUsers:
		users.append(user.username)
	return users

def getOuUsernames():
	OUs = CustomUser.objects.filter(is_currently_an_OU=True)
	users = []
	for user in OUs:
		users.append(user.username)
	return users
