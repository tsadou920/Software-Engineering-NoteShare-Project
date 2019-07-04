from django.contrib import admin
# from reversion_compare.admin import CompareVersionAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .models import *
from .forms import PostAdminForm

@admin.register(Taboo)
class TabooAdmin(admin.ModelAdmin):
    list_display = ('tabooWord', 'isPending')

    #below code hides Taboo words from non-SU's
    def get_queryset(self,request):
        # first get the default queryset for the class
        qs = super(TabooAdmin,self).get_queryset(request)
        # now, if the user is super user (attribute in ), then return all entries, otherwise return nothing
        if request.user.is_superuser:
            return qs
        return Taboo.objects.none()

    # Below code makes taboo words read-only for non-SU's
    # def get_readonly_fields(self,request,obj=None):
    #     #if the object exists and the user is not superuser
    #     if obj and not request.user.is_superuser and not request.user.is_currently_an_OU:
    #         return set([x.name for x in self.model._meta.fields])
    #     # return whatever readonly fields already exist if super user (maybe we also want some su fields to be read only too)
    #     return self.readonly_fields

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username','is_currently_an_OU','pending_OU','is_superuser']
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('CustomUser',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_currently_an_OU','pending_OU'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'is_currently_an_OU','pending_OU')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    #below code hides Taboo words from non-SU's
    def get_queryset(self,request):
        # first get the default queryset for the class
        qs = super(CustomUserAdmin,self).get_queryset(request)
        # now, if the user is super user (attribute in ), then return all entries, otherwise return nothing
        if request.user.is_superuser:
            return qs
        return CustomUser.objects.filter(username=request.user.get_username())

            

# Re-register UserAdmin
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)