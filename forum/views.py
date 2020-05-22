from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from itertools import chain
from .forms import CommunityForm, QuestionForm, AnswerForm
from .filters import QuestionFilter, CommunityFilter
from django.template.defaulttags import register

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
	answers = Answer.objects.filter(question=question)
	votedict = {}
	for answer in answers:
		upvotes = Upvote.objects.filter(answer=answer).count()
		downvotes = Downvote.objects.filter(answer=answer).count()
		votedict[answer.id] = upvotes-downvotes
	no_of_answers = answers.count()
	lst = sorted(votedict.items(), key=lambda x: x[1])
	lst.reverse()
	answers = list(Answer.objects.none())
	for x in lst:
		answers.append(Answer.objects.filter(id=x[0]))
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
		'no_of_answers': no_of_answers,
		'question': question,
		'answers': answers,
		'form': form,
		'vote': votedict,
		'get_item': get_item,
	}
	return render(request, 'forum/question_detail.html', context)

@login_required
def question_create(request, pk):
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.username = request.user
			new_form.community = Community.objects.get(id=pk)
			new_form.save()
			return redirect('/community/'+pk)
	context = {'title': 'Ask question', 'form': form}
	return render(request, 'forum/question_create.html', context)

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

@login_required
def upvote(request, pk, pk1):
	hold = Upvote.objects.filter(username=request.user, answer=Answer.objects.get(id=pk)).count()
	mike = Downvote.objects.filter(username=request.user, answer=Answer.objects.get(id=pk)).count()
	if hold==1 and mike==0:
		messages.warning(request, f'You have already upvoted the answer')
	elif hold==0 and mike==0:
		Upvote.objects.create(username=request.user, answer=Answer.objects.get(id=pk))
		messages.success(request, f'You have upvoted the answer')
	elif hold==0 and mike==1:
		Downvote.objects.filter(username=request.user, answer=Answer.objects.get(id=pk)).delete()
		messages.success(request, f'You have upvoted the answer')
	return redirect('/question/'+pk1)

@login_required
def downvote(request, pk, pk1):
	hold = Downvote.objects.filter(username=request.user, answer=Answer.objects.get(id=pk)).count()
	mike = Upvote.objects.filter(username=request.user, answer=Answer.objects.get(id=pk)).count()
	if hold==1 and mike==0:
		messages.warning(request, f'You have already downvoted the answer')
	elif hold==0 and mike==0:
		Downvote.objects.create(username=request.user, answer=Answer.objects.get(id=pk))
		messages.success(request, f'You have downvoted the answer')
	elif hold==0 and mike==1:
		Upvote.objects.filter(username=request.user, answer=Answer.objects.get(id=pk)).delete()
		messages.success(request, f'You have downvoted the answer')
	return redirect('/question/'+pk1)