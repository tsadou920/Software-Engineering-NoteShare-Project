# used in general
from django import forms

# used to create custom form for posts
from .models import Post

# used for the CustomUser Class
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Post Stuff
class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','author', 'body', 'locked', 'status')
        
        ''' Below is our attempt at censoring out the taboo words from the post - 
         it failed since Django makes sure that user-input forms are immutable probably for user integrity 
         For future improvements, we can add triggers to the Post database itself and censore that way'''
        # tabooSet = set(Taboo.objects.filter(isPending=False).values_list('tabooWord',flat=True))
        # bodyList = self.cleaned_data.get('body').strip()
        # for i in (len(bodyList)):
        #     if bodyList[i] in tabooSet:
        #         bodyList[i] = "UNK"
        # bodyString = ' '.join(bodyList)
        # self.body = bodyString
        
        # if commit:
        #     PostAdminForm.save(update_fields=['body'])
        
        # return bodyString