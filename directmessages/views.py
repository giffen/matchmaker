import datetime
from django.contrib import messages
from django.shortcuts import render, Http404, get_object_or_404
from django.contrib.auth.models import User

from .models import DirectMessage
from .forms import ComposeForm

def view_direct_message(request, dm_id):
	message = get_object_or_404(DirectMessage, id=dm_id)
	
	if message.sender != request.user and message.receiver != request.user:
		raise Http404

	if not message.read:
		message.read = datetime.datetime.now()
		message.save()

	return render(request, 'directmessages/view.html', locals())


def compose(request):
	if request.user.is_authenticated():
		
		form = ComposeForm(request.POST or None)

		if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.sent = datetime.datetime.now()
			send_message.save()

		return render(request, 'directmessages/compose.html', locals())

	else:
		messages.error(request, 'You need to be logged in to access your inbox.')
		return render(request, 'home.html', locals())

def reply(request, dm_id):
	if request.user.is_authenticated():
		parent_id = dm_id
		parent = get_object_or_404(DirectMessage, id=parent_id)

		form = ComposeForm(request.POST or None)

		if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.receiver = parent.sender
			send_message.subject = "Re: " + parent.subject
			send_message.sent = datetime.datetime.now()
			send_message.parent = parent
			send_message.save()

			parent.replied = True
			parent.save()

		return render(request, 'directmessages/compose.html', locals())

	else:
		messages.error(request, 'You need to be logged in to access your inbox.')
		return render(request, 'home.html', locals())

def inbox(request):
	if request.user.is_authenticated():
		messages_in_inbox = DirectMessage.objects.filter(receiver = request.user)
		request.session['num_of_messages'] = len(messages_in_inbox)

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

