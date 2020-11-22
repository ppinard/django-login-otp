""""""

# Standard library modules.

# Third party modules.
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

import pyotp

# Local modules.

# Globals and constants variables.


class UserManager(BaseUserManager):
    def create_user(self, email, name):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")

        user = self.model(email=self.normalize_email(email), name=name)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name):
        user = self.create_user(email, name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(models.Model):
    email = models.EmailField("email address", max_length=255, unique=True)
    name = models.CharField("full name", max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    secret = models.CharField(max_length=16, editable=False, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def save(self, *args, **kwargs):
        if self.secret is None:
            self.secret = pyotp.random_base32()
        super().save(*args, **kwargs)

    def set_password(self, *args):
        pass

    def check_password(self, otp):
        return pyotp.TOTP(self.secret).verify(otp)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def otp_url(self):
        issuer = getattr(settings, "LOGIN_OTP_ISSUER", None)
        return pyotp.TOTP(self.secret).provisioning_uri(self.email, issuer)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @property
    def is_staff(self):
        return self.is_admin
