# Advanced Permissions System

## `User` objects[(source)](https://docs.djangoproject.com/en/2.1/topics/auth/default/#user-objects)

[`User`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User) objects are the core of the authentication system. They typically represent the people interacting with your site and are used to enable things like restricting access, registering user profiles, associating content with creators etc. Only one class of user exists in Django’s authentication framework, i.e., [`'superusers'`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.is_superuser) or admin [`'staff'`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.is_staff) users are just user objects with special attributes set, not different classes of user objects.

The primary attributes of the default user are:

- [`username`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.username)
- [`password`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.password)
- [`email`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.email)
- [`first_name`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.first_name)
- [`last_name`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User.last_name)

See the [`full API documentation`](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User) for full reference, the documentation that follows is more task oriented.

## Extending the User AbstractUser notes 

The django admin interface, like the rest of django, depends on `django.contrib.auth.models` for its user models and authentication. So, if you want to add a new class of users to the django admin interfact, you need to extend that class. We're just going to add a flag called `is_OU` to differentiate between ordinary users and guest users (GU). Guest users are the default, i.e. `is_OU==False` and `is_superuser==False`. Notice that `is_superuser` is already implemented.

I first came accross [this article](https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html), but [this one](https://wsvincent.com/django-custom-user-model-tutorial/) is up to date with django 2. 

Here is an excerpt from an article that describes the process of overwriting the `AbstractUser` class to add more information to the users: 

## Django Con Notes [(source)](https://p.ota.to/blog/pushing-the-boundaries-of-the-django-admin/)

Django Suit gives sidebars and other interface elements. 

These notes are sourced from  Ola Sitarska's video from the [2016 US DJangoCon conference](https://p.ota.to/blog/pushing-the-boundaries-of-the-django-admin/).

To change the permissions, you need to override the `get_queryset(self,request)` function in any class that inherits from `admin.ModelAdmin`.

Example

```python
class EventAdmin(admin.ModelAdmin):
	list_display = ('name','organizers','date')
	search_fields = ('city','country','name')

	def get_queryset(self,request):
	# first get the default queryset for the class
	qs = super(EventAdmin,self).get_queryset(request)

	# now, if the user is super user (attribute in ), then return all entries, otherwise return all entries where the user is on that team
	if request.user.is_superuser:
		return qs
	return qs.filter(team=request.user)

```

you can also override forms by over-writing the `get_form` function, also in the class that inherits from `admin.ModelAdmin`.

```python
def get_form(self,request,obj=None,**kwargs)
	# get the original form that the superuser would see
	form = super(EventPageContentAdmin,self).get_form(request,obj,**kwargs)

	# if user is not superuser, then filter the results.
	if not request.user.is_superuser:
		if 'page' in form.base_fields:
			form.base_fields['page'].queryset = EventPage.objects.filter(event__team=request.user)

	return form

```

The `ModelAdmin` class has an option for change/edit pages called `readonly_fields` which you can use to specify that a field cannot be edited. But what if you want that feature to be conditional, where normal users can only read content that super users can create? Then you have to modify the `get_readonly_fields` method in the `ModelAdmin` class. 

Note that in this example model, they have defined a function where `is_upcoming()` is a method that returns false if an event has already passed and true if an event is coming in the future.

This code changes the `readonly_`

(20:56)
```python

def get_readonly_fields(self,request,obj=None):
	#if the object exists and the user is superuser
	if obj and not request.user.is_superuser:
	
		# and if the page is in the past
		if not obj.page.event.is_upcoming():
		
			# then set all the fields as read only
			return set([x.name for x in self.model._meta.fields])
			
	# return whatever readonly fields already exist if super user (maybe we also want some su fields to be read only too)
	return self.readonly_fields
```

This video also features info on how to display pictures on the changelist view around (22:14). Might be helpful later on.
