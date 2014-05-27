import datetime

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, Http404, get_object_or_404, HttpResponseRedirect

from .models import DirectMessage
from .forms import ComposeForm, ReplyForm

def view_direct_message(request, dm_id):
	message = get_object_or_404(DirectMessage, id=dm_id)
	
	if message.sender != request.user and message.receiver != request.user:
		raise Http404

	if not message.read:
		message.read = True
		message.read_at = datetime.datetime.now()
		message.save()

	return render(request, 'directmessages/view.html', locals())


def compose(request):
	if request.user.is_authenticated():
		title = "<h1>Compose Message</h1>"

		form = ComposeForm(request.POST or None)

		if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.sent = datetime.datetime.now()
			send_message.save()
			messages.success(request, "Message sent")
			return HttpResponseRedirect(reverse('inbox'))

		return render(request, 'directmessages/compose.html', locals())

	else:
		messages.error(request, 'You need to be logged in to access your inbox.')
		return render(request, 'home.html', locals())

def reply(request, dm_id):
	if request.user.is_authenticated():
		parent_id = dm_id
		parent = get_object_or_404(DirectMessage, id=parent_id)

		title = "<h1>Reply <small>%s from %s</small></h1>" %(parent.subject, parent.sender)

		form = ReplyForm(request.POST or None)

		if form.is_valid():
			send_message = form.save(commit=False)
			send_message.sender = request.user
			send_message.receiver = parent.sender
			send_message.subject = "Re: " + parent.subject
			send_message.sent = datetime.datetime.now()
			send_message.parent = parent
			send_message.save()
			messages.success(request, "Reply sent")
			path = reverse('view_direct_message', args=dm_id)
			return HttpResponseRedirect(path)

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

