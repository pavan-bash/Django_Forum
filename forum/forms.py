from django import forms
from .models import Community, Question, Answer, ReportQ, ReportA, ReplyAnswer
from pagedown.widgets import PagedownWidget

class CommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = ['name', 'desc']

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'desc', 'tags', 'add_new_tag']

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['desc']
		
class ReplyForm(forms.ModelForm):
	class Meta:
		model = ReplyAnswer
		fields = ['desc']

class ReportQForm(forms.ModelForm):
	class Meta:
		model = ReportQ
		fields = ['reason', 'desc']

class ReportAForm(forms.ModelForm):
	class Meta:
		model = ReportA
		fields = ['reason', 'desc']