from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
	return render(request, 'home.html', locals())

def all(request):

	users = User.objects.filter(is_active=True)

	return render(request, 'all.html', locals())