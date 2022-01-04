from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserChangeForm, MyUserCreationForm
from django.contrib.auth import get_user_model


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = get_user_model()
    list_display = ('username',  'is_staff', 'is_active')
    list_filter = ('username',  'is_staff', 'is_active')
    fieldsets = ((None, {'fields': ('username',  'password')}),
                 ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',  'password1', 'password2', 'is_staff', 'is_active', )}
        ),
    )
    search_fields = (
        'username',

    )
    ordering = (
        'username',

    )
    filter_horizontal = ()


admin.site.register(get_user_model(), MyUserAdmin)
