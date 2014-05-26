from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from matchmaker.apis import secret_key

import stripe
stripe.api_key = secret_key

class Address(models.Model):
	user = models.ForeignKey(User)
	street_address = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	zipcode = models.IntegerField(max_length=10)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.city

class Job(models.Model):
	user = models.ForeignKey(User)
	position = models.CharField(max_length=100)
	employer = models.CharField(max_length=200)
	employer_address = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	zipcode = models.IntegerField(max_length=10)
	phone = models.CharField(max_length=20, null=True, blank=True)
	start_date = models.DateField(auto_now=False, auto_now_add=False)
	end_date = models.DateField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	active = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.position

class UserPicture(models.Model):
	user = models.ForeignKey(User)
	image = models.ImageField(upload_to='profiles/')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return str(self.image)

CHOICES = (
	('Regular', 'Regular'),
	('Staff', 'Staff'),
	('Premium', 'Premium'),
)

class UserRole(models.Model):
	user = models.OneToOneField(User)
	role = models.CharField(max_length=120, default='Regular', choices=CHOICES)

	def __unicode__(self):
		return self.role


class UserStripe(models.Model):
	user = models.OneToOneField(User)
	stripe_id = models.CharField(max_length=120, null=True, blank=True)

	def __unicode__(self):
		return self.user.username

	def get_stripe_id(self):
		return self.stripe_id

def CreateStripeId(sender, user, request, **kwargs):
	new_id, created = UserStripe.objects.get_or_create(user=user)
	if created:
		# add users email to stripe, then set the stripe ID.
		stripe_cust = stripe.Customer.create(email = user.email, description="Customer for %s" %user.email)
		new_id.stripe_id = stripe_cust.id 
		new_id.save()
	else:
		print "Not Created"

user_logged_in.connect(CreateStripeId)