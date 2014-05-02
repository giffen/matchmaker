from django.contrib import admin

from .models import Address, Job

class AddressAdmin(admin.ModelAdmin):
	class Meta:
		model = Address

admin.site.register(Address, AddressAdmin)

class JobAdmin(admin.ModelAdmin):
	class Meta:
		model = Job

admin.site.register(Job, JobAdmin)