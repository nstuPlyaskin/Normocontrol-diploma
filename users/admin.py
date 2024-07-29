from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Group


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (
            None, {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'allow_manage'
                    )
            }
        ),
    )
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'pk',
        'group',
        'allow_manage',
        'username',
        'email',
    )
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug',)
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = "-пусто-"


admin.site.register(Group, GroupAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
