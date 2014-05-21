from django.db import models
from django.contrib.auth.models import User

class MatchManager(models.Manager):
	def user_matches(self, user):
		matches = []
		if self.filter(from_user=user).count() > 0:
			obj = Match.objects.filter(from_user=user)
			for x in obj:
				if x.to_user != user:
					matches.append(x.to_user)
		if self.filter(to_user=user).count() > 0:
			obj = Match.objects.filter(to_user=user)
			for x in obj:
				if x.from_user != user:
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

class Match(models.Model):
	to_user = models.ForeignKey(User, related_name='match')
	from_user = models.ForeignKey(User, related_name='match2')
	percent = models.DecimalField(max_digits=10, decimal_places=4, default=.75)

	objects = MatchManager()

	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.percent