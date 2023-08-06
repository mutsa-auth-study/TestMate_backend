import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin   # 사용자 권한 부여
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields): # 프로필 사진 등
        if not email: # email 없을 시 error
            raise ValueError('must have user email')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        superuser = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        superuser.save()
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('NAME', max_length=20)
    uname = models.CharField('UNAME', max_length=20, blank=True, null=True)
    email = models.EmailField('EMAIL', max_length=40, unique=True)
    age = models.IntegerField('AGE', null=True, blank=True)
    GENDER_CHOICES = ( ('M', 'Male'), ('F', 'Female') )
    gender = models.CharField('GENDER', max_length=1, choices=GENDER_CHOICES)
    def upload_to_func(instance, filename):
        prefix = timezone.now().strftime("%Y/%m/%d")
        file_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()
        return "/".join(
            [prefix, file_name, extension, ]
        )
    image = models.ImageField('IMAGE', upload_to=upload_to_func, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    following_set = models.ManyToManyField('self', symmetrical=False, related_name='follower_set', blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.uname or ''

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser
