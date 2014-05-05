from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	user = models.ForeignKey(User)
	question = models.CharField(max_length=120)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return self.question


class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length=120)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return self.answer