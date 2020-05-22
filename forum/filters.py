import django_filters
from django_filters import DateFilter

from .models import *

class QuestionFilter(django_filters.FilterSet):
	class Meta:
		model = Question
		fields = {'title': ['icontains', ]}

class CommunityFilter(django_filters.FilterSet):
	class Meta:
		model = Community
		fields = {'name': ['icontains', ]}
