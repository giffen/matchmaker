from django.contrib import admin

from .models import DirectMessage

class DirectMessageAdmin(admin.ModelAdmin):
	#list_display = ['from_user','to_user','percent']
	class Meta:
		model = DirectMessage

admin.site.register(DirectMessage, DirectMessageAdmin)
