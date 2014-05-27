from django.contrib import messages
from django.shortcuts import render, Http404
from django.contrib.auth.models import User

from .models import DirectMessage

def inbox(request):
	if request.user.is_authenticated():
		messages_in_inbox = DirectMessage.objects.filter(receiver = request.user)

		return render(request, 'directmessages/inbox.html', locals())

	else:
		messages.error(request, 'You need to be logged in to access your inbox.')
		return render(request, 'home.html', locals())

	
def sent(request):
	if request.user.is_authenticated():
		messages_sent = DirectMessage.objects.filter(sender = request.user)

		return render(request, 'directmessages/sent.html', locals())

	else:
		messages.error(request, 'You need to be logged in to access your inbox.')
		return render(request, 'home.html', locals())

