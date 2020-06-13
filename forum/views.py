from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from itertools import chain
from .forms import CommunityForm, QuestionForm, AnswerForm, ReportQForm, ReportAForm, ReplyForm
from .filters import QuestionFilter, CommunityFilter
from django.template.defaulttags import register
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Count

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def home(request):
	if request.user.is_authenticated:
		communities = CommunityJoin.objects.filter(username=request.user)
		questions = CommunityJoin.objects.none()  # To create empty QuerySet
		for community in communities:
			x = Question.objects.filter(community=Community.objects.filter(name=community)[0])
			questions = questions | x
	else:
		questions = Question.objects.all().order_by('-date_asked')
	myFilter = QuestionFilter(request.GET, queryset=questions)
	questions = myFilter.qs
	context = {'title': 'Home', 'questions': questions, 'filter': myFilter}
	return render(request, 'forum/home.html', context)

@login_required
def all_questions(request):
	questions = Question.objects.all().order_by('-date_asked')
	myFilter = QuestionFilter(request.GET, queryset=questions)
	questions = myFilter.qs
	context = {'title': 'Popular', 'questions': questions, 'filter': myFilter}
	return render(request, 'forum/all_questions.html', context)

def about(request):
	context = {'title': 'About'}
	return render(request, 'forum/about.html', context)

def login_question(request, pk):
	if request.user.is_authenticated:
		hold = CommunityJoin.objects.filter(communityname=Community.objects.get(id=pk), username=request.user)
		if hold.count():
			return redirect("/"+pk+"/ask_question/")
		else:
			messages.warning(request, f'You should be a member of this community')
			return redirect("/community/"+pk)
	else:
		return redirect("/login/?next=/"+pk+"/ask_question/")

def question_detail(request, pk):
	question = Question.objects.get(id=pk)
	answers = Answer.objects.filter(question=question).annotate(count=Count('likes')).order_by('-count')
	replydict = {}
	is_liked = {}
	total_likes = {}
	for answer in answers:
		replydict[answer.id] = ReplyAnswer.objects.filter(answer=answer)
		is_liked[answer.id] = False
		if answer.likes.filter(id=request.user.id).exists():
			is_liked[answer.id] = True
		total_likes[answer.id] = answer.total_likes()
	
	form = AnswerForm()
	if request.method == 'POST':
		if request.user.is_authenticated:
			form = AnswerForm(request.POST)
			if form.is_valid():
				new_form = form.save(commit=False)
				new_form.username = request.user
				new_form.question = question
				new_form.save()
				return redirect('/question/'+pk)
		else:
			return redirect("/login/?next=/question/"+pk)
	context = {
		'title': 'Home',
		'question': question,
		'answers': answers,
		'form': form,
		'replydict': replydict,
		'is_liked': is_liked,
		'total_likes': total_likes,
		'get_item': get_item,
		'tags': question.tags.all(),
	}
	return render(request, 'forum/question_detail.html', context)

def question_detail_reply(request, pk, pk1):
	question = Question.objects.get(id=pk)
	answers = Answer.objects.filter(question=question).annotate(count=Count('likes')).order_by('-count')
	replydict = {}
	is_liked = {}
	total_likes = {}
	for answer in answers:
		replydict[answer.id] = ReplyAnswer.objects.filter(answer=answer)
		is_liked[answer.id] = False
		if answer.likes.filter(id=request.user.id).exists():
			is_liked[answer.id] = True
		total_likes[answer.id] = answer.total_likes()
		
	form = AnswerForm()
	dynamicform = ReplyForm()
	if request.method == 'POST':
		if request.user.is_authenticated:
			form = AnswerForm(request.POST)
			dynamicform = ReplyForm(request.POST)

			if form.is_valid() and dynamicform.is_valid():
				new_form = dynamicform.save(commit=False)
				new_form.username = request.user
				new_form.answer = Answer.objects.get(id=pk1)
				new_form.save()
				return redirect('/question/'+pk)
		else:
			return redirect("/login/?next=/question/"+pk)
	context = {
		'title': 'Home',
		'question': question,
		'answers': answers,
		'form': form,
		'form1': dynamicform,
		'replydict': replydict,
		'is_liked': is_liked,
		'total_likes': total_likes,
		'get_item': get_item,
		'reply_answer': Answer.objects.get(id=pk1),
		'tags': question.tags.all(),
	}
	return render(request, 'forum/question_detail_reply.html', context)

@login_required
def question_create(request, pk):
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.username = request.user
			new_form.community = Community.objects.get(id=pk)
			if new_form.add_new_tag!=None:
				Tag.objects.create(name=new_form.add_new_tag)			
			new_form.save()
			form.save_m2m()
			return redirect('/community/'+pk)
	context = {'title': 'Ask question', 'form': form}
	return render(request, 'forum/question_create.html', context)

@login_required
def question_edit(request, pk):
	question = Question.objects.get(id=pk)
	form = QuestionForm(request.POST or None, instance=question)
	if form.is_valid():
		form.save()
		return redirect('/question/'+pk)
	context = {'title': 'Edit Question', 'form': form}
	return render(request, 'forum/question_edit.html', context)

@login_required
def answer_edit(request, pk):
	answer = Answer.objects.get(id=pk)
	form = AnswerForm(request.POST or None, instance=answer)
	if form.is_valid():
		form.save()
		return redirect('/question/'+str(answer.question.id))
	context = {'title': 'Edit Answer', 'form': form}
	return render(request, 'forum/answer_edit.html', context)

def community_detail(request, pk):
	community = Community.objects.get(id=pk)
	questions = Question.objects.filter(community=community)
	no_of_questions = questions.count()
	if request.method == 'POST':
		if request.user.is_authenticated:
			if CommunityJoin.objects.filter(username=request.user, communityname=community).count():
				messages.warning(request, f'You have already a member of this community')
			else:
				CommunityJoin.objects.create(username=request.user, communityname=community)
				messages.success(request, f'You are now a member of "{community.name}" community')
				return redirect("my_communities")
		else:
			return redirect("/login/?next=/community/"+pk)
	context = {
		'title': community.name,
		'no_of_questions': no_of_questions,
		'community': community,
		'questions': questions,
	}
	return render(request, 'forum/community_detail.html', context)

def community(request):
	communities = Community.objects.all().order_by('-date_created')
	myFilter = CommunityFilter(request.GET, queryset=communities)
	communities = myFilter.qs
	context = {'title': 'Communities', 'communities': communities, 'filter': myFilter}
	return render(request, 'forum/community.html', context)	

@login_required
def my_communities(request):
	joins = CommunityJoin.objects.filter(username=request.user)
	context = {'title': 'My Communities', 'joins': joins}
	return render(request, 'forum/my_communities.html', context)	

@login_required
def community_create(request):
	form = CommunityForm()
	if request.method == 'POST':
		form = CommunityForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.username = request.user
			new_form.save()
			community = Community.objects.all().last()
			CommunityJoin.objects.create(username=request.user, communityname=community)
			messages.success(request, f'You are now the leader of the "{community.name}" community')
			return redirect('my_communities')
	context = {'title': 'Create Community', 'form': form}
	return render(request, 'forum/community_create.html', context)


def like_answer(request):
	answer = Answer.objects.get(id=request.POST.get('id'))
	is_liked = {}
	total_likes = {}
	is_liked[answer.id] = False
	if answer.likes.filter(id=request.user.id).exists():
		answer.likes.remove(request.user)
		is_liked[answer.id] = False
	else:
		answer.likes.add(request.user)
		is_liked[answer.id] = True
	total_likes[answer.id] = answer.total_likes()
	context = {
		'answer': answer,
		'is_liked': is_liked,
		'total_likes': total_likes,
	}
	if request.is_ajax():
		html = render_to_string('forum/like_section.html', context, request=request)
		return JsonResponse({'form': html})

@login_required
def reportqtest(request, pk):
	question = Question.objects.get(id=pk)
	if request.user==question.username:
		messages.warning(request, f'You cannot report your question')
		return redirect("/question/"+pk)
	if ReportQ.objects.filter(question=question, username=request.user).count():
		messages.warning(request, f'You have already reported this question')
		return redirect("/question/"+pk)
	else:
		return redirect("/reportq/"+pk)

@login_required
def reportq(request, pk):
	question = Question.objects.get(id=pk)
	form = ReportQForm()
	if request.method == 'POST':
		form = ReportQForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.username = request.user
			new_form.question = question
			new_form.save()
			messages.success(request, f'Your reponse has been recorded')
			return redirect("/question/"+pk)
	context = {'title': 'Report Question', 'question': question, 'form': form}
	return render(request, 'forum/reportq.html', context)

@login_required
def reportatest(request, pk):
	answer = Answer.objects.get(id=pk)
	if request.user==answer.username:
		messages.warning(request, f'You cannot report your answer')
		return redirect("/question/"+str(answer.question.id))
	if ReportA.objects.filter(answer=answer, username=request.user).count():
		messages.warning(request, f'You have already reported this answer')
		return redirect("/question/"+str(answer.question.id))
	else:
		return redirect("/reporta/"+pk)

@login_required
def reporta(request, pk):
	answer = Answer.objects.get(id=pk)
	form = ReportAForm()
	if request.method == 'POST':
		form = ReportAForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.username = request.user
			new_form.answer = answer
			new_form.save()
			messages.success(request, f'Your reponse has been recorded')
			return redirect("/question/"+str(answer.question.id))
	context = {'title': 'Report Answer', 'answer': answer, 'form': form}
	return render(request, 'forum/reporta.html', context)

def tag_detail(request, pk):
	tag = Tag.objects.filter(name=pk)[0]
	questions = Question.objects.all()
	tag_questions = Question.objects.none()
	for question in questions:
		q = Question.objects.filter(id=question.id)
		if question.tags.filter(name=pk).exists():
			tag_questions = q | tag_questions
		if question.add_new_tag == pk:
			tag_questions = q | tag_questions

	context = {'title': 'Tag Filter', 'questions': tag_questions, 'tag': tag}
	return render(request, 'forum/tag_questions.html', context)	