from django.contrib import admin

from .models import Question, Answer, UserAnswer

class QuestionAdmin(admin.ModelAdmin):
	class Meta:
		model = Question

admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
	class Meta:
		model = Answer

admin.site.register(Answer, AnswerAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
	class Meta:
		model = UserAnswer

admin.site.register(UserAnswer, UserAnswerAdmin)

