from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

# show the tier field in the admin panel
UserAdmin.fieldsets += ('Tier', {'fields': ('tier',)}),

# add the tier field in the list of default fields
UserAdmin.list_display += ('tier',)