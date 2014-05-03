from django.shortcuts import render, Http404
from django.contrib.auth.models import User

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
	address = Address.objects.get(user=user)
	job = Job.objects.get(user=user)
	picture = UserPicture.objects.get(user=user)

	address_form = AddressForm(request.POST or None, prefix='address', instance=address)
	job_form = JobForm(request.POST or None, prefix='job', instance=job)
	user_picture_form = UserPictureForm(request.POST or None, prefix='pic', instance=picture)
	
	if address_form.is_valid() and job_form.is_valid() and user_picture_form.is_valid():
		form1 =  address_form.save(commit=False)
		form1.save()
		form2 =  job_form.save(commit=False)
		form2.save()
		form3 =  user_picture_form.save(commit=False)
		form3.save()

	return render(request, 'profiles/edit_profile.html', locals())	