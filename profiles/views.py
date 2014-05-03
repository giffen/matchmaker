from django.shortcuts import render, Http404
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

from .models import Address, Job, UserPicture 
from .forms import AddressForm, JobForm, UserPictureForm

def home(request):
	return render(request, 'home.html', locals())

def all(request):

	users = User.objects.filter(is_active=True)

	return render(request, 'profiles/all.html', locals())

def single_user(request, username):
	
	try:
		user = User.objects.get(username=username)
		if user.is_active:
			single_user = user
	except:
		raise Http404
	
	return render(request, 'profiles/single_user.html', locals())

def edit_profile(request):
	user = request.user #grabs the logged in user
	picture = UserPicture.objects.get(user=user)

	user_picture_form = UserPictureForm(request.POST or None, prefix='pic', instance=picture)
	
	addresses = Address.objects.filter(user=user)
	AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
	formset_a = AddressFormset(request.POST or None, queryset=addresses)

	jobs = Job.objects.filter(user=user)
	JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
	formset_j = JobFormset(request.POST or None, queryset=jobs)

	if user_picture_form.is_valid():
		form3 =  user_picture_form.save(commit=False)
		form3.save()

	return render(request, 'profiles/edit_profile.html', locals())

def edit_address(request):
	user = request.user #grabs the logged in user
	addresses = Address.objects.filter(user=user)
	AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
	formset_a = AddressFormset(request.POST or None, queryset=addresses)

	if formset_a.is_valid():
		pass

	return render(request, 'profiles/edit_address.html', locals())

def edit_job(request):
	user = request.user #grabs the logged in user
	jobs = Job.objects.filter(user=user)
	JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
	formset_j = JobFormset(request.POST or None, queryset=jobs)
	
	if formset_j.is_valid():
		pass

	return render(request, 'profiles/edit_jobs.html', locals())	