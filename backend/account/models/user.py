
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _




class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, contact_name, email, password=None):
        if not email:
            raise ValueError('user must have email')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.contact_name = contact_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('user must have email')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):

    username = models.NOT_PROVIDED
    email = models.EmailField(_('email address'), unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
