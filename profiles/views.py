from django.contrib import messages
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.shortcuts import render, Http404, HttpResponseRedirect

from questions.matching import points, match_percentage
from matches.models import Match, JobMatch
from .models import Address, Job, UserPicture 
from .forms import AddressForm, JobForm, UserPictureForm


def home(request):
	return render(request, 'home.html', locals())

def all(request):

	users = User.objects.filter(is_active=True)
	try:
		matches = Match.objects.user_matches(request.user)
	except Exception:
		pass

	return render(request, 'profiles/all.html', locals())

def single_user(request, username):
	
	try:
		user = User.objects.get(username=username)
		if user.is_active:
			single_user = user
	except:
		raise Http404

	set_match, created = Match.objects.get_or_create(from_user=request.user, to_user=single_user)
	
	match_percentage(request.user,single_user)
	
	set_match.percent = round(match_percentage(request.user, single_user), 4)
	set_match.good_match = Match.objects.good_match(request.user, single_user)
	set_match.save()
	

	if set_match.good_match:
		single_user_jobs = Job.objects.filter(user=single_user)
		if len(single_user_jobs) > 0:
			for job in single_user_jobs:
				job_match, created = JobMatch.objects.get_or_create(user=request.user, job=job)
				job_match.save()

	match = set_match.percent * 100
	return render(request, 'profiles/single_user.html', locals())

def edit_profile(request):
	user = request.user #grabs the logged in user
	picture = UserPicture.objects.get(user=user)

	user_picture_form = UserPictureForm(request.POST or None, request.FILES or None, prefix='pic', instance=picture)
	
	addresses = Address.objects.filter(user=user)
	AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
	formset_a = AddressFormset(queryset=addresses)

	jobs = Job.objects.filter(user=user)
	JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
	formset_j = JobFormset(queryset=jobs)

	if user_picture_form.is_valid():
		form3 =  user_picture_form.save(commit=False)
		form3.save()

	return render(request, 'profiles/edit_profile.html', locals())

def edit_locations(request):
	if request.method == 'POST':
		user = request.user #grabs the logged in user
		addresses = Address.objects.filter(user=user)
		AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
		formset_a = AddressFormset(request.POST or None, queryset=addresses)

		if formset_a.is_valid():
			for form in formset_a:
				new_form = form.save(commit=False)
				new_form.user = request.user
				new_form.save()

			messages.success(request, 'Profile details updated.')
		else:
			messages.error(request, 'Profile details did not update.')

		#return render(request, 'profiles/edit_address.html', locals())
		return HttpResponseRedirect('/edit/')
	else:
		raise Http404

def edit_jobs(request):
	if request.method == 'POST':
		user = request.user #grabs the logged in user
		jobs = Job.objects.filter(user=user)
		JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
		formset_j = JobFormset(request.POST or None, queryset=jobs)
	
		if formset_j.is_valid():
			for form in formset_j:
				new_form = form.save(commit=False)
				new_form.user = request.user
				new_form.save()
				
			messages.success(request, 'Profile details updated.')
		else:
			messages.error(request, 'Profile details did not update.')

		#return render(request, 'profiles/edit_address.html', locals())
		return HttpResponseRedirect('/edit/')
	else:
		raise Http404