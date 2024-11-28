from django.contrib import admin
from .models import User, UserConfirmation, Achievement


admin.site.register(User)
admin.site.register(UserConfirmation)
admin.site.register(Achievement)
