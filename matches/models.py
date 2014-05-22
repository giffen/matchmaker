from django.db import models
from django.contrib.auth.models import User

from profiles.models import Job

class MatchManager(models.Manager):
	def user_matches(self, user):
		matches = []
		if self.filter(from_user=user).count() > 0:
			obj = Match.objects.filter(from_user=user)
			for x in obj:
				if x.to_user != user:
					if Match.objects.good_match(abc.to_user, user):
						matches.append(x.to_user)
		if self.filter(to_user=user).count() > 0:
			obj = Match.objects.filter(to_user=user)
			for x in obj:
				if x.from_user != user:
					if Match.objects.good_match(abc.from_user, user):
						matches.append(x.from_user)
		return matches

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