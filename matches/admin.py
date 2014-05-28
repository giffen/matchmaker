from django.contrib import admin

from .models import Match, JobMatch, MatchList

class MatchAdmin(admin.ModelAdmin):
	list_display = ['from_user','to_user','percent']
	class Meta:
		model = Match

admin.site.register(Match, MatchAdmin)

class JobMatchAdmin(admin.ModelAdmin):
	list_display = ['user','job']
	class Meta:
		model = JobMatch

admin.site.register(JobMatch, JobMatchAdmin)

class MatchListAdmin(admin.ModelAdmin):
	class Meta:
		model = MatchList

admin.site.register(MatchList, MatchListAdmin)