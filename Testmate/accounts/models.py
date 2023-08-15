import os
from uuid import uuid4
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

        # 파일 업로드 경로 생성 함수 정의
    def upload_to_func(instance, filename):
        prefix = timezone.now().strftime("%Y/%m/%d")
        file_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()
        return "/".join(
            [prefix, file_name, extension, ]
        )
    

    username = models.CharField(max_length=150,default='')
    user_id = models.CharField('아이디',max_length=20)
    profile_nickname = models.CharField('닉네임', max_length=20, blank =True, null=True)
    profile_image =  models.ImageField('프로필 사진', upload_to=upload_to_func, null=True, blank=True)
    email = models.CharField('이메일', max_length=40, unique=True)


    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

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

