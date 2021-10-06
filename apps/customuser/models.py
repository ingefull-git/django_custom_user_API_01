from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(
                email=email,
                username=username,
                **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, username, password, **other_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email         = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username      = models.CharField(max_length=30, unique=True)
    created       = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    login         = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)


    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

