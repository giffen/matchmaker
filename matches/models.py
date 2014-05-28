from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from profiles.models import Job

class MatchList(models.Model):
	user = models.ForeignKey(User, related_name='main_user')
	match = models.ForeignKey(User, related_name='matched_user')
	read = models.BooleanField(default=False)
	read_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.user.username)

	class Meta:
		ordering = ['-updated','-timestamp']

def login_user_matches(sender, user, request, **kwargs):	
		obj = Match.objects.filter(from_user=user)
		for x in obj:
			if x.to_user != user:
				if Match.objects.good_match(x.to_user, user):
					add_to_list, created = MatchList.objects.get_or_create(user=user, match=x.to_user)
		obj2 = Match.objects.filter(to_user=user)
		for x in obj2:
			if x.from_user != user:
				if Match.objects.good_match(x.from_user, user):
					add_to_list, created = MatchList.objects.get_or_create(user=user, match=x.from_user)

		request.session['new_matches_count'] = MatchList.objects.filter(user=user).filter(read=False).count()

user_logged_in.connect(login_user_matches)


class MatchManager(models.Manager):
	def are_matched(self, user1, user2):
		if self.filter(from_user=user1, to_user=user2).count() > 0:
			obj = Match.objects.get(from_user=user1, to_user=user2)
			perc = obj.percent * 100
			return perc
		if self.filter(from_user=user2, to_user=user1).count() > 0:
			obj = Match.objects.get(from_user=user2, to_user=user1)
			perc = obj.percent * 100
			return perc
		else:
			return False

	def good_match(self, user1, user2):
		obj = Match.objects.all()
		per = []
		for i in obj:
			per.append(i.percent)

		avg_per = reduce(lambda x, y: x+y, per)/len(per) * 100

		if self.are_matched(user1, user2) >= avg_per:
			return True
		else:
			return False

class Match(models.Model):
	to_user = models.ForeignKey(User, related_name='match')
	from_user = models.ForeignKey(User, related_name='match2')
	percent = models.DecimalField(max_digits=10, decimal_places=4, default=.75)
	good_match = models.BooleanField(default=True)

	objects = MatchManager()

	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.percent

class JobMatch(models.Model):
	user = models.ForeignKey(User)
	job = models.ForeignKey(Job, null=True, blank=True)
	show = models.BooleanField(default=True)

	def __unicode__(self):
		return self.job.position