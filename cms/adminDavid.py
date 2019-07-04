from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import PostAdminForm#, CustomUserCreationForm, CustomUserChangeForm
from operator import attrgetter
from itertools import chain


#admin.site.register(Post) #this displays all class elements of Post to be edited. Equivalent to putting every attribute in list_display
def make_lock(modeladmin, request, queryset):
		queryset.update(locked=True)
make_lock.short_description = "Mark selected posts as locked"


def make_unlock(modeladmin, request, queryset):
		queryset.update(locked=False)
make_unlock.short_description = "Mark selected posts as unlocked"

@admin.register(Post) #this line does the same thing as admin.site.register(Post), but lets you also create your own ModelAdmin class to choose what you display in the admin interface
class PostAdmin(CompareVersionAdmin):
	list_display = ('title', 'slug', 'author','publish','status','locked') #this doesn't let you edit such things like the date created
	list_filter = ('status', 'created', 'publish','author')
	actions = [make_lock, make_unlock]
	search_fields = ('title','body')
	#prepopulated_fields = {'slug':('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ('status','publish')
	form = PostAdminForm
	def get_queryset(self,request):
		# first get the default queryset for the class
		qs = super(PostAdmin,self).get_queryset(request)
		# now, if the user is super user (attribute in ), then return all entries, otherwise return nothing
		if request.user.is_superuser:
			return qs
		author_list = qs.filter(author=request.user)
		filter_args = {'inviteTo': request.user, 'isAccepted': True}
		filter_args = dict((k,v) for k,v in filter_args.items() if v is not None)
		invites_list = Invitation.objects.filter(**filter_args)
		if invites_list:
			permissions_list = Post.objects.filter(id=invites_list[0].post.id)
			for i in range(1, len(invites_list)):
				permissions_list = permissions_list | Post.objects.filter(id=invites_list[i].post.id)
			result_list = author_list | permissions_list
			return result_list
		return author_list