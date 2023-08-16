import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,AbstractUser   # 사용자 권한 부여
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

# 사용자 관리자 클래스 정의
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:  # 이메일이 없을 때 오류 발생
            raise ValueError('이메일은 필수 항목입니다.')

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
            raise ValueError('슈퍼유저는 is_superuser=True 여야 합니다.')

        superuser = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        superuser.save()
        return superuser


# 사용자 모델 클래스 정의
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('이메일', unique=True)

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    kakao_id = models.BigIntegerField('카카오 아이디', null=True, blank=True)
    profile_nickname = models.CharField('닉네임', max_length=20, null=True, blank=True)
    profile_image = models.CharField('프로필 사진', max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

