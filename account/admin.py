from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.models import Group

from .models import UserBase, Profile, Review


@admin.register(UserBase)
class AccountAdmin(BaseUserAdmin):

    fieldsets = (
        ('Account Information', {"fields": ('email', 'username', 'password', 'first_name','last_name','slug')}),
        ('Permissions', {"fields": ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), "classes": ('collapse',)}),
        ('Important dates', {'fields': ('last_login',), "classes": ('collapse',)})
    )

    list_display = ('username', 'email', 'slug', 'id', 'is_staff', 'is_active', 'last_login' )
    list_filter = ['is_active', 'is_staff', 'groups']
    search_fields = ['email', 'username', 'id', 'slug']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Account Information', {"fields": ('user', 'stars', 'star_count', 'interests', 'about', 'image', 'slug')}),
        )

    list_display = ('user', 'id', 'slug')
    list_filter = [ 'id']
    search_fields = ['user__username', 'id', 'slug']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Review Information', {"fields": ('user', 'rate', 'opinion')}),
        )

    list_display = ('user', 'id', 'rate')
    list_filter = [ 'user', 'rate']
    search_fields = ['user__username', 'id', 'rate']



class GroupAdminForm(forms.ModelForm):
    """
    ModelForm that adds an additional multiple select field for managing
    the users in the group.
    """
    users = forms.ModelMultipleChoiceField(
        UserBase.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Users', False),
        required=False,
        )


    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_users = self.instance.user_set.values_list('pk', flat=True)
            self.initial['users'] = initial_users


    def save(self, *args, **kwargs):
        kwargs['commit'] = True
        return super(GroupAdminForm, self).save(*args, **kwargs)


    def save_m2m(self):
        self.instance.user_set.clear()
        self.instance.user_set.add(*self.cleaned_data['users'])

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    """
    Customized GroupAdmin class that uses the customized form to allow
    management of users within a group.
    """
    form = GroupAdminForm
