# from socket import fromshare
# from attr import fields
# from attr import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import ModelForm

from .models import *

# from .models import Owner
# class OwnerForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password1', 'password2', ]


class RegisterForm(UserCreationForm):

    # sid         = forms.IntegerField(label="Student Id", required=True)

    # department  = forms.CharField(max_length=150, required=True)

    # id_card_pic = forms.ImageField(required=True)

    # fb_profile  = forms.URLField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "password1", "password2", "name", "number")

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ["email", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    # # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_student = True
    #     user.save()
    #     student = Student.objects.create(user=user, sid = self.sid, department = self.department, id_card_pic = self.id_card_pic, fb_profile = self.fb_profile)
    #     return user


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ("sid", "fb_profile", "id_card_pic", "department")


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = ("nid_card_pic",)


class MessForm(ModelForm):
    class Meta:
        model = Mess
        fields = (
            'gender',
            'name',
            'region',
            'structure',
            'meal_system',
            'students_num',
            'distance',
            'address',
            'image1',
            'image2',
            'image3',
        )


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ('room_no', 'bed_num', 'price', 'floor', 'status', 'image1', 'image2', 'image3')

    # def __init__(self, *args, **kwargs):
    #     super(RoomForm, self).__init__(*args, **kwargs)
        # self.fields["mess"].disabled = True
        # self.fields["email"].disabled = True
