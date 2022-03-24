from distutils.command.upload import upload
import email
from random import choices
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
# from platformdirs import site_data_dir
# from pyparsing import makeXMLTags
# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import gettext as _
# # Create your models here.


# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(_)

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    number = models.CharField(max_length=14, unique=True)
    profile_pic = models.ImageField(blank= True,upload_to ='profile/')

    is_student = models.BooleanField(default= 0) #1 for student, 0 for owner

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    print("ok")
    objects = CustomUserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email

    def __str__(self):
        return str(self.email)


class Student(models.Model):
    department_choices = (
        (2, 'CSE'),
        (3, 'EEE'),
        (4, 'ECE'),
        (1, 'Agriculture'),
        (5, 'DVM'),
        (6, 'Physics'),
    )
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    sid = models.IntegerField(primary_key=True)
    department = models.IntegerField(choices=department_choices)

    id_card_pic = models.ImageField(blank = True)

    fb_profile = models.URLField(blank=True)

    def __str__(self):
        return self.user.name


class Owner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

    nid_card_pic = models.ImageField()

    def __str__(self):
        return self.user.name


class Mess(models.Model):
    region_choices = (
        (1, 'Mohabolipur'),
        (2, 'Suvra'),
        (3, 'Kornai'),
        (4, 'BKSP')
    )
    gender_choices = (
        (1, 'Male'),
        (2, 'Female')
    )
    cooking_system_choices = (
        (1, 'Meal'),
        (2, 'Bati'),
        (3, 'On Your Own')
    )
    structure_choices = (
        (1, 'Multi-storey'),
        (2, 'Single-storey'),
        (3, 'Tin Shed')
    )

    id              = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=100)
    owner           = models.OneToOneField(Owner, on_delete=models.CASCADE)
    region          = models.IntegerField(choices = region_choices)
    gender          = models.IntegerField(choices = gender_choices)
    cooking_system  = models.IntegerField(choices = cooking_system_choices)
    structure       = models.IntegerField(choices = structure_choices)
    students_num    = models.IntegerField()

    distance        = models.IntegerField() #in meter

    def __str__(self):
        return self.name

class MessImages(models.Model):
    mess        = models.ForeignKey(Mess, on_delete=models.CASCADE)
    image       = models.FileField(upload_to='Mess_Gallery')
    
    def __str__(self):
        return self.mess.name

class Room(models.Model):
    bed_num_choice = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )
    status_choice = (
        (0, 'Not Available'),
        (1, 'Available')
    )

    id          = models.AutoField(primary_key=True)
    room_no     = models.IntegerField()
    bed_num     = models.IntegerField(choices = bed_num_choice)
    mess        = models.ForeignKey(Mess, on_delete=models.CASCADE)
    price       = models.IntegerField()
    floor       = models.IntegerField(default=0)
    status      = models.BooleanField(default=1)
    picture      =models.ImageField()

    def __str__(self):
        return str(self.room_no)


class RoomImages(models.Model):
    room        = models.ForeignKey(Room, on_delete=models.CASCADE)
    image       =models.FileField(upload_to='Room_Gallery')
    
    def __str__(self):
        return self.room.mess.name + " - " + str(self.room.room_no)



# class Comment(models.Model):
#     id      = models.AutoField(primary_key=True)
#     content = models.TextField()
#     user    = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
#     room    = models.ForeignKey(Room, on_delete=models.CASCADE)
#     created = models.DateField(auto_now_add=True)
#     # updated = models.DateField(auto_now=True)

#     def __str__(self):
#         return self.content[:10]