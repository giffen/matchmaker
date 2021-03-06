from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer, UserAnswer,MatchAnswer

#Mandatory == 300
#Very Important == 100
#Somewhat Important == 20
#Not Important == 0

def assign_points(query):
	if query == "Mandatory":
		return 300
	elif query == "Very Important":
		return 100
	elif query == "Somewhat Important":
		return 20
	elif query == "Not Important":
		return 0

def all_questions(request):
	questions_all = Question.objects.all()
	paginator = Paginator(questions_all, 1)
	important_levels = ['Mandatory', 'Very Important', 'Somewhat Important', 'Not Important']

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
		#user answer
		answer_form =  request.POST['answer']
		importance_level =  request.POST['importance_level']

		#user match answer
		match_answer_form =  request.POST['match_answer']
		match_importance_level =  request.POST['match_importance_level']

		user = User.objects.get(username=request.user)
		question = Question.objects.get(id = question_id)

		# user answer save
		answer = Answer.objects.get(question=question, answer=answer_form)
		answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = answer
		answered.importance_level = importance_level
		answered.points = assign_points(importance_level)
		answered.save()

		# user match answer save
		user_answer = Answer.objects.get(question=question, answer=match_answer_form)
		answered, created = MatchAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = user_answer
		answered.importance_level = match_importance_level
		answered.points = assign_points(match_importance_level)
		answered.save()

		messages.success(request, 'Answer saved.')

	return render(request, 'questions/all.html', locals())
