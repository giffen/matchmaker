from django.shortcuts import render, Http404
from django.contrib.auth.models import User

def home(request):
	return render(request, 'home.html', locals())

def all(request):

	users = User.objects.filter(is_active=True)

	return render(request, 'all.html', locals())

def single_user(request, username):
	
	try:
		user = User.objects.get(username=username)
		if user.is_active:
			single_user = user
	except:
		raise Http404
	
	return render(request, 'single_user.html', locals())