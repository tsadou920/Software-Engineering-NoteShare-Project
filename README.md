# Noteshare Install Instructions

First, clone this repositor and install `virtualenv` which creates a separate environment for your python code. `virtualenv`  is a program that allows you to run specific versions of the python libraries you import. More info here a quick summary can be found in this [stackoverflow post](https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe), and more info can be found in the [virtualenv documentation](https://virtualenv.pypa.io/en/latest/userguide/). 

```shell
pip install virtualenv
```

Then, navigate to the root folder of this github repo (the directory where the readme is) and run this command.

```
virtualenv NoteShare
```

After that, tell virtualenv to use your latest version of python.

```
virtualenv NoteShare -p `which python`
```
Then navigate into the `NoteShare` directory with 

```
cd NoteShare
```

Next, activate your virtual environment

```
source ./bin/activate
```
After all this, you can finally install django with 

```
pip	install	Django==2.0.5
```

And you can check if everything has been installed correctly by executing the following command and observing the output. 

```
pip list
```

If you want to quit `virtualenv`, type 

```
deactivate
```
To start the virtual environment after deactivating, simply activate it once again 

```
source ./bin/activate
```

# Dependencies
After you've set up the python virtual environment, install the necessary dependencies with
```
pip install django-reversion
pip install django-reversion-compare
pip install admin_view_permission
```

# NoteShare

NoteShare will be a note-taking software system designed technical high schools, colleges, and after school programs. The app enables students to share study guides and notes related to programming, algorithms and data structures. 

Essentially, each class in the school is a separate user group. Each class has a class president who act as a Super User to moderate the creation of study guides. Within the class, some students may choose to participate in using the application, while others do not. Students who participate by sharing their notes or helping to add to or edit other’s notes have full access to edit and view the class’ study guides. We call these students Ordinary Users. However, students who decline to participate will be Guest Users with more limited access.

This application could be especially helpful in schools where teachers have limited time and resources to dedicate to each student. However, the main purpose of this application is to foster community among classmates, so they can help one another through school.  

We want to develop a document sharing system such that group members can collaborate on the same documents without causing inconsistencies. There are three types of users in this system: Super User (SU), Ordinary User (OU) and Guest (GU). 

## Specification + Implementation Notes
unless otherwise noted, I'm drawing from [this page](https://docs.djangoproject.com/en/2.1/ref/contrib/admin/) in the django documentation.

### SU: 

- update membership 
  - Todo(David) add the IsOU option to the user change page also to the add user page.
  - **DONE** (Ana) SU can select isOU and pendingOU at the user creaation and user change forms.

- maintain a list of "taboo" words 
  - **DONE** (Ana) create a new model for taboo words, then [register](https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#the-register-decorator) the model in `admin.py`. A link to the taboo list will appear on the **admin index** page, while the list itself will appear in the **change list** page.

- unlock any locked document 
  - **DONE** (Angelika) a locked or unlocked column/attribute to the posts/notes model. This should appear automatically on the **add or change** django page.

- process complaints about OU's 
  - **DONE** (Hua) create a complaints model, then register in `admin.py`  A link to the complaints list will appear on the **admin index** page, while the list itself will appear in the **change list** page.


### OU: 
- create new document(s), 
  - **DONE** (David)
- the creator of a document is the owner of the document 
  - **DONE** (David) how to establish ownership through the **add or change** page. Might need to override methods in admin.py like [this](https://stackoverflow.com/questions/48700888/django-admin-how-to-check-model-instance-belong-to-owner-before-deleting).
    - Note that the owner and author are the same thing. Authors can share their post with other users through invitations

- creator of a document can invite other OUs to update it
  - **DONE** (Angelika) create invitations model, with foreign key relationship to documents/posts
  - Todo (David) way to add search to an invitations field AND display a list of people invited on the **add or change** page.
    **DONE** (but still needs to be tested with multiple users)
- creator of a document can decide if the document is 
  - open to the public (can be seen by everyone)
  - restricted (can only be viewed as read-only by GU's and edited by OU's), 
  - shared (viewed/edited by OU's who are invited) and private  
  	- add open/restricted/shared option to posts model `privacy = models.CharField(max_length=10,choices=PRIVACY_CHOICES,default='private')` where `PRIVACY_CHOICES` is a list of tuples similar to `STATUS_CHOICES` already in `models.py`

- an OU can accept or deny the invitation(s) placed by other OUs for their documents 
  - **DONE** (Ana) OU only sees their documents and the ones they have been invited to (and accepted the invitation)
  - need an invitation requests model/table that has as columns:
  	- foreign key: userTO, the user the inviation is sent to
  	- foreign key: userFROM, the user the invitation was sent from
  	- slug, the slug (unique id) of the document in question


- lock a shared document for updating, only one OU can lock a document successfully, the system should indicate which OU is updating the document **DIDN'T DO"** due to conflict with ModelAdmin structure. 
- update a successfully locked document, and then assign a unique version sequence number and remember who and when makes the updates **DIDN'T DO"** due to conflict with ModelAdmin structure.

- unlock a shared document locked by him/herself 
	**DONE**~(Angelika)
- file complaints to the owner of a document about other OUs'updates or to the SU about the owner of the documents 
  - need another model for file complaints. similar implementation to file invitation. 
	- **DONE** (Hua)
- as the owner of a document deal with complaints filed by other OUs (remove some OUs who were invited before) 
	- **DONE** (Hua)

- unlock the locked documents s/he owns that is being updated by others 
	- **DONE** (Angelika) posts need to be filtered.

- search own file(s) based on (partial) keyword
	- **DONE** (David)

- search information about other OUs based on name and/or interests. 
	- **DONE** (David) seach based on name.  
- have all privileges for GUs 

### GU: 
- read open document(s), retrieve old version(s) of open document(s) and complains about those documents.
	- **DONE**: (David)

- apply to be an OU that is to be confirmed or rejected by SU, in the application his/her name, technical interests should be submitted.
	- **DONE** (David), but without techical interests
constraints: 

- there is only ONE current version for any document
  - **Done** (David)
- for simplicity there is only one word for each line in all documents 
  - ***Done*** (David): Need to somehow validate entry with the clean() function here too.
- only the editing command(s) are saved for older versions with three possible actions: 
  - add, 
  - delete
  - update. 
   - ***Done*** (David): Check the python difflib documentation for update syntax.
- For instance, if the file doc_1.txt contains one line "the", and doc_2.txt contains three lines "welcome \n the \n world\n", then your system only saves doc_2.txt, doc_1.history saves the commands "delete 1; delete 3" which changes doc_2.txt into doc_1.txt. Your system generates the history command file based on the difference. 
- the retrieval of older versions of documents should be done by your system based on the current version and possibly a sequence of history files. 
  - **Done** (David)
- any word(s) belonging to the taboo list (maintained by SU) are replaced by UNK by the system, and the one who use these words are warned automatically, s/he should update the document next time s/he log in the system as the first job (all other activities are blocked) 
  - **Didn't Do** (David and Ana): Django admin forms are immutable and we currently have not found a work around that to replace contents of the body field of the post
```diff
- You can find commented out code for the save() function in /NoteShare/cms/forms.py to see our attempts at censoring the user post form.
```
  

  - ***Done*** (David): More than one word per line needs further testing. Differences just trail off the screen and individual words are not accounted for. 
- a GUI is required
  - **Done** (David)
- different users should have their own page populated by his/her picture and 3 most recent documents. For a brand-new user, the 3 most popular (most read and/or updated) files in the system are shown. 


# Original Specification

SU: 

- update membership 

- maintain a list of "taboo" words 

- unlock any locked document 

- process complaints about OU's 

- have all privileges reserved for OUs inside any group 

  OU: 

- create new document(s), the creator of a document is the owner of the document and can invite other OUs to update it, and decide if the document is open to the public (can be seen by everyone), restricted (can only be viewed as read-only by GU's and edited by OU's), shared (viewed/edited by OU's who are invited) and private 

- an OU can accept or deny the invitation(s) placed by other OUs for their documents 

- lock a shared document for updating, only one OU can lock a document successfully, the 

  system should indicate which OU is updating the document 

- update a successfully locked document, and then assign a unique version sequence number 

  and remember who and when makes the updates 

- unlock a shared document locked by him/herself 

- file complaints to the owner of a document about other OUs'updates or to the SU about the 

  owner of the documents 

- as the owner of a document deal with complaints filed by other OUs (remove some OUs 

  who were invited before) 

- unlock the locked documents s/he owns that is being updated by others 

- search own file(s) based on (partial) keyword 

- search information about other OUs based on name and/or interests. 

- have all privileges for GUs 

  GU: 

- read open document(s), retrieve old version(s) of open document(s) and complains about those documents. 

- send suggestions to SU about taboo words 

- apply to be an OU that is to be confirmed or rejected by SU, in the application his/her name, technical interests should be submitted. 

constraints: 

- there is only ONE current version for any document 

- for simplicity there is only one word for each line in all documents 

- only the editing command(s) are saved for older versions with three possible actions: add, 

  delete and update. For instance, if the file doc_1.txt contains one line "the", and doc_2.txt contains three lines "welcome \n the \n world\n", then your system only saves doc_2.txt, doc_1.history saves the commands "delete 1; delete 3" which changes doc_2.txt into doc_1.txt. Your system generates the history command file based on the difference. 

- the retrieval of older versions of documents should be done by your system based on the current version and possibly a sequence of history files. 

- any word(s) belonging to the taboo list (maintained by SU) are replaced by UNK by the system, and the one who use these words are warned automatically, s/he should update the document next time s/he log in the system as the first job (all other activities are blocked) 

- a creative feature worthy of 15% is required for each system, one possible feature could be allowing more than word per line, or speech-based document updating is allowed, or some machine learning features to render this system adaptable/evolving by itself thru usage. 

- a GUI is required, different users should have their own page populated by his/her picture and 3 most recent documents. For a brand-new user, the 3 most popular (most read and/or updated) files in the system are shown. 




