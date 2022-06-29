import imp

from django.contrib import admin
from django.contrib.auth import admin as admin_auth_django

from .forms import UserChangeForm, UserCreationForm
from .models import Users

# Register your models here.

@admin.register(Users)
class UsersAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
 