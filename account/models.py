from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone

from programmingLanguage.models import Language



def user_directory_path(instance, filename):
    return f'profile_images/{instance.id}/{filename}'


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Custom Manager
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.username}-user')
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("account:profile", kwargs={'slug':self.profile.slug})


    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'ProgrammingCenter Team',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Language, related_name='user_interests', blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    about = models.TextField(blank=True)
    image = models.ImageField(default='avatar.png', upload_to=user_directory_path)
    stars = models.ManyToManyField(UserBase, related_name='star', default=None, blank=True)
    star_count = models.BigIntegerField(default='0')

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user.username}-profile')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("account:profile", kwargs={'slug':self.slug})

    def __str__(self):
        return self.user.username

class Review(models.Model):
    RATE_CHOICES = [
        (1,'Terrible'),
        (2,'Bad'),
        (3,'OK'),
        (4,'Good'),
        (5,'Excellent')
        ]

    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    opinion = models.TextField(blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse("account:review_results")

    def __str__(self):
        return self.user.username
    
