""""""

# Standard library modules.

# Third party modules.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

# Local modules.
from .models import User

# Globals and constants variables.


class UserAuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    password = forms.CharField(
        label="One time password", max_length=6, min_length=6, widget=forms.TextInput()
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and one-time password. "
            "Note that both fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "name")


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "name", "is_active", "is_admin")


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    change_form_template = "useradmin/change_form.html"

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "name", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        ("Username", {"fields": ("email",)}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_admin", "is_active")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "name"),},),)
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.login_form = UserAuthenticationForm
admin.site.unregister(Group)
