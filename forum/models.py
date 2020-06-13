from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField

class Community(models.Model):
    name = models.CharField(max_length = 200, null=True, unique=True)
    desc = models.TextField()
    username = models.ForeignKey(User, verbose_name="Maker of the Community", null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
       return self.name    

class Question(models.Model):
    title = models.CharField(max_length=200, null=True, unique=True)
    desc = RichTextUploadingField(null=True)
    date_asked = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User, verbose_name="Questioned by", on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    is_reported = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    add_new_tag = models.CharField(max_length=200, null=True, blank=True, unique=True)

    #def save(self, *args, **kwargs):
    #    try:
    #        if add_new_tag:
    #            Tag.objects.create(name=add_new_tag)
    #    except:
    #        pass
    #      super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})

class Answer(models.Model):
    username = models.ForeignKey(User, verbose_name="Answered by", null=True, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    desc = RichTextUploadingField(null=True)
    is_reported = models.BooleanField(default=False)
    date_answered = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.desc

class CommunityJoin(models.Model):
	communityname = models.ForeignKey(Community, null=True, on_delete= models.CASCADE)
	username = models.ForeignKey(User, verbose_name="Community joined by", null=True, on_delete= models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.communityname.name

class ReportQ(models.Model):

    choices = (
        ('not_belong', 'It does not belong to this community'),
        ('rules', 'It breakes the rules of the community '),
        ('spam', 'spam'),
        ('others', 'others'),
        )

    question = models.ForeignKey(Question, null=True, on_delete= models.CASCADE)
    username = models.ForeignKey(User, verbose_name="Reporter of the question", null=True, on_delete= models.CASCADE)
    reason = models.CharField(max_length=300, null=True, choices = choices)
    date_reported = models.DateTimeField(auto_now_add=True, null=True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.question.title

class ReportA(models.Model):

    choices = (
        ('irrelevent', 'It is an irrelevent answer'),
        ('content', 'It has explicit content'),
        ('spam', 'spam'),
        ('others', 'others'),
        )

    answer = models.ForeignKey(Answer, null=True, on_delete= models.CASCADE)
    username = models.ForeignKey(User, verbose_name="Reporter of the answer", null=True, on_delete= models.CASCADE)
    reason = models.CharField(max_length=300, null=True, choices = choices)
    date_reported = models.DateTimeField(auto_now_add=True, null=True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.answer.desc

class ReplyAnswer(models.Model):
    username = models.ForeignKey(User, verbose_name="Replied by", null=True, on_delete= models.CASCADE)
    desc = models.TextField()
    date_replied = models.DateTimeField(auto_now_add=True, null=True)
    answer = models.ForeignKey(Answer, null=True, on_delete= models.CASCADE)

    def __str__(self):
        return self.answer.desc    