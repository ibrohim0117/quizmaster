from django.contrib import admin
from .models import User, UserConfirmation, Achievement


# admin.site.register(User)
# admin.site.register(UserConfirmation)
admin.site.register(Achievement)


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ['code', 'expiration_time', 'is_confirmed', 'user', 'id']
    search_fields = ['is_confirmed', ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'levels', 'roles', 'is_verified', 'is_superuser', 'ball', 'id']
    search_fields = ['email', ]

