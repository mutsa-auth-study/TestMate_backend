from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class CustomUserAdmin(UserAdmin):
    # 폼 설정
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('user_id', 'profile_nickname', 'profile_image', 'email')
    list_filter = ('is_superuser',)

    # fieldsets = (
    #     (None, {'fields': ('email', 'password',)}),
    #     ('Personal info', {'fields':('user_id', 'profile_nickname', 'profile_image', 'email')}),
    #     ('Permissions', {'fields': ('is_superuser',)}),
    # )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('name', 'password1', 'password2')}
    #     ),
    # )
    search_fields = ('email',)
    ordering = ('user_id',)
    filter_horizontal = ()



admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)