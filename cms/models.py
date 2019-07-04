from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
import uuid

class CustomUser(AbstractUser):
    is_currently_an_OU = models.BooleanField(default=False)
    pending_OU = models.BooleanField(default=False)

class Post(models.Model):
	STATUS_CHOICES = (
		('public','Public'),
		('restricted','Restricted'),
		('shared','Shared'),
		('private','Private')
		)
	title = models.CharField(max_length=250)
	 # slugs are short labels that has only letters, numbers, underscores. It's used to create a unique 
	 	#(search engine friendly) url for each post. the unique_for_date='publish' argument notifies django
	 	# to prevent multiple posts from having the same slug, if they happen to to have the same date
	slug = models.SlugField(max_length=250,unique_for_date='publish')
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='blog_posts') #many to one relationship: every post 
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='public')
	locked = models.BooleanField(default=False)
	
	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

class Complaint(models.Model):
	#User = models.ForeignKey(User)
	complainAbout = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='complainee')
	commplainFrom = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='complainant',blank=True, null=True)
	#commplainFrom = models.ForeignKey(editable = False)
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='postComplaint',blank=True, null=True)
	explanation = models.TextField()
	


class Invitation(models.Model):
	inviteTo = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='inviteTo')
	inviteFrom = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='inviteFrom',blank=True, null=True)
	isAccepted = models.BooleanField(default=False)
	isApplication = models.BooleanField(default=False) 
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name = 'postInvite')
	#invite_id = models.AutoField(primary_key=True)  
	
class Taboo(models.Model):
	tabooWord = models.CharField(max_length=20)
	isPending = models.BooleanField(default=True)


# for ana's text class implement a solution that validates the text from the body text box to make sure
# each word is on a separate line of text (use python string methods to do this). If not, return an 
# error message to the user. 

# more on returning messages in admin interface: https://docs.djangoproject.com/en/2.0/ref/contrib/messages/
# more on model validation with clean() https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#overriding-modelform-clean-method

# for finding the differences between text blocks, you could use the difflib library
# https://stackoverflow.com/questions/19120489/compare-two-files-report-difference-in-python
