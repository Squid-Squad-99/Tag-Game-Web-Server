from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserChangeForm, MyUserCreationForm
from django.contrib.auth import get_user_model


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = get_user_model()
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('username', 'email', 'is_staff', 'is_active')
    fieldsets = ((None, {'fields': ('username', 'email', 'password')}),
                 ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'birth_day',)}
        ),
    )
    search_fields = (
        'username',
        'email',
    )
    ordering = (
        'username',
        'email',
    )
    filter_horizontal = ()


admin.site.register(get_user_model(), MyUserAdmin)
