from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.core.urlresolvers import reverse
from django.db import models

# Possible suffixes for names.
SUFFIX_CHOICES = (
    ('', '---------'),
    ('S', 'Sr.'),
    ('J', 'Jr.'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV')
)


class PensieveUserManager(BaseUserManager):

    def _create_user(self, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        """Creates and saves a user with the given email, name, and password."""
        if not email:
            raise ValueError('Email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(email, first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name, last_name, password, True, True, **extra_fields)


class PensieveUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=256, unique=True)
    first_name = models.CharField('first name', max_length=30)
    middle_name = models.CharField('middle name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30)
    suffix = models.CharField('suffix', choices=SUFFIX_CHOICES, max_length=5, default='')
    nickname = models.CharField('nickname', max_length=30, blank=True,
                                help_text='The name a user prefers to be called.')
    maiden_name = models.CharField('maiden name', max_length=30, blank=True)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    birthday = models.DateField('birthday', blank=True, null=True)

    objects = PensieveUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return reverse('profiles.detail', kwargs={'email': self.email})

    def get_full_name(self):
        """Return the user's full name, in the format 'First[ Middle] Last[, Suffix]'."""
        suffix = (self.suffix != '')
        values = (self.first_name,
                  ' ' if self.middle_name else '',
                  self.middle_name,
                  self.last_name,
                  ',' if suffix and (self.suffix in ['J', 'S']) else '',
                  ' ' if suffix else '',
                  self.get_suffix_display() if suffix else '')
        return '%s%s%s %s%s%s%s' % values

    def get_short_name(self):
        """Return the user's nickname, if defined, or first name otherwise."""
        return self.nickname or self.first_name

    def get_common_name(self):
        """Return the user's nickname (if defined; first name otherwise) and last name."""
        return '%s %s' % (self.get_short_name(), self.last_name)
