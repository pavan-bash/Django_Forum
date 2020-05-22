from django import forms
from .models import Community, Question, Answer

class CommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['name', 'desc']

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'desc']

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['desc']
