from django.contrib.auth.models import User
from django.shortcuts import render, Http404, HttpResponseRedirect

from .models import Question, Answer, UserAnswer

def all_questions(request):
	questions = Question.objects.all()

	if request.method == "POST":
		question_id =  request.POST['question_id']
		answer_form =  request.POST['answer']

		user = User.objects.get(username=request.user)
		question = Question.objects.get(id = question_id)
		answer = Answer.objects.get(question=question, answer=answer_form)

		answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = answer
		answered.save()

	return render(request, 'questions/all.html', locals())
