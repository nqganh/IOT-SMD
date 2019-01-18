from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from fields import ContentTypeRestrictedFileField


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^user\.fields\.ContentTypeRestrictedFileField"])

ADMIN = 1
CUSTOMER = 2
#BUYER = 3

class UserManager(BaseUserManager):
    def create_user(self, email, password = None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an username')

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password = password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, error_messages={ 'unique': 'Email address already exists in the system.' }, unique=True)
    sure_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    is_staff = models.BooleanField(default=False, verbose_name='staff', help_text='Designates whether the user can log into this admin site.')

    role = models.IntegerField(default=ADMIN, choices=((ADMIN, 'ADMIN'),(CUSTOMER, 'CUSTOMER')))
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
    # address information
    address = models.CharField(max_length=1000, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email
