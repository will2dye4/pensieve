from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import PensieveUser


class AdminUserCreationForm(UserCreationForm):
    """A form that creates a user, with no privileges, from the given email, name, and password."""

    def __init__(self, *args, **kwargs):
        super(AdminUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PensieveUser
        fields = ('email', 'first_name', 'last_name',)


class AdminUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on the user, but replaces the
    password field with admin's password hash display field."""

    def __init__(self, *args, **kwargs):
        super(AdminUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PensieveUser
        exclude = ()
