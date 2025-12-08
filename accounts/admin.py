from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone', 'email', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات', {'fields': ('full_name', 'email')}),
        ('دسترسی', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('phone', 'password1', 'password2'),
        }),
    )

    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()



# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)