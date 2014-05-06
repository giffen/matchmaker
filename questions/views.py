from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer, UserAnswer

def all_questions(request):
	questions_all = Question.objects.all()
	paginator = Paginator(questions_all, 1)

	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		questions = paginator.page(paginator.num_pages)


	if request.method == "POST":
		question_id =  request.POST['question_id']
		answer_form =  request.POST['answer']

		user = User.objects.get(username=request.user)
		question = Question.objects.get(id = question_id)
		answer = Answer.objects.get(question=question, answer=answer_form)

		answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = answer
		answered.save()

		messages.success(request, 'Answer saved.')

	return render(request, 'questions/all.html', locals())
