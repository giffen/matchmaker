from django.contrib.auth.models import User
from django.shortcuts import render, Http404, HttpResponseRedirect

from .models import Question, Answer

def all_questions(request):
	questions = Question.objects.all()

	return render(request, 'questions/all.html', locals())
