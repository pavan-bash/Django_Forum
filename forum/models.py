from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Community(models.Model):
    name = models.CharField(max_length = 200, null=True, unique=True)
    desc = models.TextField()
    username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=200, unique=True)
    desc = models.TextField()
    date_asked = models.DateTimeField(default=timezone.now)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})

class Answer(models.Model):
	username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
	question = models.ForeignKey(Question, null=True, on_delete= models.CASCADE)
	date_answered = models.DateTimeField(default=timezone.now)
	desc = models.TextField()

	def __str__(self):
		return self.desc

class CommunityJoin(models.Model):
	communityname = models.ForeignKey(Community, null=True, on_delete= models.CASCADE)
	username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.communityname.name

class Upvote(models.Model):
    answer = models.ForeignKey(Answer, null=True, on_delete= models.CASCADE)
    username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    date_voted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username.username

class Downvote(models.Model):
    answer = models.ForeignKey(Answer, null=True, on_delete= models.CASCADE)
    username = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    date_voted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username.username