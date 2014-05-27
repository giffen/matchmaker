from django.db import models

from django.contrib.auth.models import User

class DirectMessage(models.Model):
	subject = models.CharField(max_length=150)
	body = models.CharField(max_length=3000)
	sender = models.ForeignKey(User, related_name='sent_direct_messages', null=True, blank=True)
	receiver = models.ForeignKey(User, related_name='received_direct_messages', null=True, blank=True)
	sent = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	read = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

	def __unicode__(self):
		return self.subject
