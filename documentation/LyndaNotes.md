# Learning Django Lynda Notes

## Installation

- Install the latest version of python, if you don't have it already.

- Install Django with `pip3 install Django==2.1.2` since, as of now, 2.1.2 is the latest edition.

- To create a django project, navigate to a folder in terminal and then issue the command`django-admin.py start project <project name>` . On linux, you may need to run this command with `sudo`.

- to build an app, navigate to your project, then type, `python3 manage.py startapp <name of new app>` 

- the difference between an app and a project according to [stack overflow](https://stackoverflow.com/questions/19350785/what-s-the-difference-between-a-project-and-an-app-in-django-world) :

  > *project* refers to the entire application and all its parts.
  >
  > An *app* refers to a submodule of the project. It's  self-sufficient and not intertwined with the other apps in the project  such that, in theory, you could pick it up and plop it down into another  project without any modification.  An *app* typically has its own *models.py*  (which might actually be empty).  You might think of it as a standalone  python module.  A simple project might only have one app.
  >
  > For your example, the *project* is the whole website. You might structure it so there is an *app* for articles, an *app* for ranking tables, and an *app*  for fixtures and results.  If they need to interact with each other,  they do it through well-documented public classes and accessor methods.
  >
  > The main thing to keep in mind is this level of interdependence between the *apps*. In practice it's all one *project*,  so there's no sense in going overboard, but keep in mind how  co-dependent two apps are.  If you find one app is solving two problems,  split them into two apps.  If you find two apps are so intertwined you  could never reuse one without the other, combine them into a single app.

- From the *Django 2 by Example* Book:

  >In Django, a project is considered a Django installation with some settings. An application	is a group of models, views, templates, and URLs.

- whenever you create a new Django, go into the `settings.py` file in your project folder and add your new app to the `INSTALLED_APPS` list.

- each of the files in a django app, has a purpose:

  | File or Folder | Purpose                              |
  | -------------- | ------------------------------------ |
  | apps.py        | configuration and initialization     |
  | models.py      | Data Layer                           |
  | admin.py       | administrative interface             |
  | urls.py        | url routing                          |
  | views.py       | control layer                        |
  | tests.py       | test the app                         |
  | migrations/    | directory that holds migration files |

# Django's MVC

Django uses a different Model-View-Controller architecture than most. Here's the terminology in focus:

- url patterns `urls.py` : details where to go when a url request is made
- views `views.py`: these are functions that take url requests and return views.
- templates `templates/` these are what is returned by functions in views.py
- models `models.py` views may draw upon data structures found here to compute what they need to compute.

## Models

- Models are just python classes that inherit from `models.Model` ; each model represent sql tables (models are an orm?). 

```python
from django.db import models
class Item(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	amount = models.IntegerField()
```

- there are lots of field types that may or may not correspond to data types in various sql databases
- some fields are used to establish foreign key, or primary key relationships
- `max_length=200`  in line 3 is a field attribute. 
- Keep in mind the difference between field attributes `blank=` and `null=` which can be set to true or false. `blank` means that the cell is empty, `null` means it contains the python null.
- You can also establish choices (like in a drop-down menu) without making a new model (table) of options, but using the  `choices=` field attribute. `sex = models.CharField(choices=SEX_CHOICES, max_length=1, blank = True)` where `SEX_CHOICES` is a list of tuples `[('M','Male')('F','Female')]`. The  first tuple value is what is stored in the database, and the second value is used for display in forms and in the django admin.
- For foreign keys do this:

```python
vaccinations = models.ManyToManyField('Vaccine',blank=True)
#here vaccinations is a field in the Pets model and the string argument to the 
#ManyToManyField() function, 'Vaccine', is the name of the table to which this
# key serves as foreign key 
```

## Migrations

- whenever you add a model, add or remove a  field ( column) from a model or whenever you edit a field, you have to migrate those changes to the database.
- migration commands include 
  - `python manage.py makemigrations` 
    - inspects the differences between the current models and the exiting database models 
    - creates a **migration files** which outlines steps that need to be taken to make the database match the models.
    - migration files are kept in the`appname/migrations/` directory. these files are automatically numbered (starting with 1.)
  - `python manage.py migrate` 
    - this command actually runs the migration files and runs all the migrations that have not yet been run already
    - you can also migrate the models of just one specific app with one specific migration file: `python manage.py migrate <appname> <number>` . The number is the filename of the migration you want to apply. Again, those migration files are held in `appname/migrations/` .
  - `python3 manage.py showmigrations` is the command you need to show the migrations (duh). When an x appears in the brackets, the migration has been applied, otherwise it hasn't.
    - migrations can be a common source of development error, so when two developers experience different outputs, but have the same code, check their migrations folder and run this command to see which migrations have been run and in what order.
  - If you ever want to see the sql that a migration would execute, use the following command `python3 manage.py sqlmigrate <appname> <number>` the `<number>` is the number of the migration you'd like to turn to sql, for example: If I had `0001_initial.py` in the migrations directory of my app, then I would use `0001` as my number. 
- ==Question==: how do you link the models to the sqlite database? Is it automatic when it comes to migrations?

### When to Migrate

- **Adding a Model :** whenever you add a new table, you need to do what's called an "initial migration" to get the data held in model from the pyhton interpreter to the database.

- **Adding , Removing or Changing a Field:** whenever you add a new field (which will appear as a new column in your database once you migrate it), you need to migrate. Same goes for removing or changing a field.

  ****

## Django ORM

- say you want to import a pet model into your code. import the file dotted with the class name of the model like so: `from <fileName>.models import <modelName>` for example, importing the pet model from adoptions.py looks like`from adoptions.models import Pet`.
- access all rows of the model with `Pet.object.all()`
- if you want to access all elements of the attribute in question, say the number of vaccinations a pet has, you can use `Pet.vaccinations.all()`
- access the model attributes by dotting them after the model name egoogle.com. `Pet.name`. no parentheses needed. Not a member function. 
- you can query the model with `Pet.objects.get(id=1,name='Pepe')` . The get command will return an error if the query results in two or more records; it's like an assignment with an sql table.

# Notes from Django 2 by Example

## Django ORM

### Creating and Updating Objects
- If you want to add an entry to the database, then you don't need to migrate (that's just for changing the structure of a table--renaming/deleting/adding columns)
- Instead of a migration, you simply save your changes with the `<objectName>.save()` method after all your desired changes have been made.
- Note that this the `User.objects.get()` method will raise a `DoesNotExist` exception if it can't find a row that matches your query.
- If  `User.objects.get()` returns more than one result, it  will  raise a `MultipleObjectsReturned` exception.
- Keep these exceptions in mind when writing code, by including a `try:` and `except:` block that handles these errors.

```python
from  django.contrib.auth.models  import  User # this is for the get method
from  cms.models import  Post #this is model I defined in the cms app need to import for Post() constructor

# retrieve username from db with get method
user  = User.objects.get(username='admin')
# declare a post in memory with Post() constructor
post  = Post(title='Another post',
  slug='another-post',
  body='Post  body.',
  author=user)
# now save the post to to db (same as SQL INSERT)
post.save()

```
- The previous code snippet shows how to create an object in memory and *then* persist it into the databse.
- The next snippet allows us to do both steps at once, should we need to have changes executed right away.
```python
Post.objects.create(title='One more post',  slug='one-more-post', body='Post body.', author=user)
```
- One reason why you might want to separate in-memory declaration and database change is if you want to modify an object after declaring it. For example, if I wanted to change the title of the pst we declared, I'd write `>> post.title  = 'New  title'` then `post.save()`.

### Retrieving Objects
- The Django  object-relational mapping uses **QuerySets** which are a collection of objects from your database that can have several filters to limit the results.
- Each Django model has at least one **manager**, and the default manager is called **objects**. You can call objects with dot notation like in `all_posts  = Post.objects.all()` which makes `all_posts` an identifier for all the posts at once.
- *filters* are basically SQL WHERE clauses that can be written one of two ways:
```python
Post.objects.filter(publish__year=2017, author__username='admin')

Post.objects.filter(publish__year=2017) \
                        .filter(author__username='admin')
```
- `exclude()` is the opposite of filter. Here you designate qualities you'd like to leave out.
- `order_by()` can order by ascending and descending. To return a descending order, negate your attribute inside the quotes `Post.objects.order_by('-title')`. To retrieve your query in ascending order, remove the negation.

- after assigning an object to an identifier, you can delete the object. Deleting  objects will  also  delete  any dependent relationships for ForeignKey  objects defined with  `on_delete` set to  `CASCADE`.
```python
post  = Post.sobjects.get(id=1)
post.delete()
```

### Query Set Evaluation
- You can chain multiple query sets together, but the query won't be sent to the database until it has been evaluated.
==this was unclear in the text== when are query sets evaluated and what does "evaluated" mean?

### Model Managers
- In the "Retrieving Objects" section of this document, we mentioned that "Each Django model has at least one **manager**, and the default manager is called **objects** as in`Post.objects.all()`.
- Managers are just classes that define what query functions we can execute. Why would you need more than one manager? Say you want to write a lot of code that manipulates published posts. Instead of writing the queries like `Post.objects.filter(status='published',title__startswith='Who')`, you can reduce the number of filter arguments by defining a new filter in a new manager:

```python
class PublishedManager(models.Manager):
  def get_queryset(self):
    return  super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
        # ...
        # you have to declare each of the managers in your model, when you define your own
        # note: these are managers, not fields; they don't reperesent columns in databasetable
        objects = models.Manager()  # The default manager.
        published = PublishedManager()  # Our custom  manager.
```

- With the code shown above, we can execute queries like `Post.published.(title__startswith='Who')`, where `published` is a new manager.
- The `get_queryset()`  is a method that returns the QuerySet that will be  executed. We override this method to include our custom filter in the final QuerySet
# Personal Project Tutorial (with Bootstrap) Lynda Notes
