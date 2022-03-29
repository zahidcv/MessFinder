from ctypes import Structure
from email import message

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render

from MainApp.models import *

from .forms import *


def shome(request):

    return render(request, "shome.html", {})


def register(request):

    return render(request, "init_register.html", {})


def StudentRegister(request):
    formbasic = RegisterForm
    formstudent = StudentForm

    if request.method == "POST":
        formbasic = RegisterForm(request.POST)
        formstudent = StudentForm(request.POST)

        # print('printing request.post ')
        print(request.POST)
        if formbasic.is_valid():
            form_b = formbasic.save(commit=False)
            form_b.is_student = True
            form_b.save()
            print(formbasic.cleaned_data.get("email"))
            print("-------Printing form_b--------")
            print(type(form_b))
        else:
            print("basic invalid")
        print("..........Custom User Obejct........")
        print(
            CustomUser.objects.filter(email=formbasic.cleaned_data.get("email")).first()
        )

        if formstudent.is_valid():
            form_s = formstudent.save(commit=False)

            form_s.user = CustomUser.objects.filter(
                email=formbasic.cleaned_data.get("email")
            ).first()
            form_s.save()
            print(formstudent.cleaned_data.get("department"))
        else:
            print("stduent invalid")
            # for field in formbasic:
            #     for error in field.errors:
            #         print(error)
        for field in formbasic:
            for error in field.errors:
                print(error)
        return HttpResponse("Successful")

    dic = {"formbasic": formbasic, "formstudent": formstudent}

    return render(request, "student_register.html", context=dic)


def OwnerRegister(request):
    formbasic = RegisterForm
    formowner = OwnerForm

    if request.method == "POST":
        formbasic = RegisterForm(request.POST)
        formowner = OwnerForm(request.POST, request.FILES)

        # print('printing request.post ')
        # print(request.POST)
        if formbasic.is_valid() and formowner.is_valid():
            form_b = formbasic.save(commit=False)
            form_b.is_student = False
            # print("-------Printing form_b--------")
            print(type(form_b))
            form_b.save()
            # print(formbasic.cleaned_data.get("email"))

            # print(type(form_b))

            form_o = formowner.save(commit=False)

            form_o.user = form_b
            form_o.save()
            print("form owner successfully saved")
            return redirect("login")
        else:
            if not formbasic.is_valid():
                print("basic invalid")
            if not formowner.is_valid():
                print("owner invalid")

            for field in formowner:
                for error in field.errors:
                    print(error)

            for field in formbasic:
                for error in field.errors:
                    print(error)

            return render(
                request,
                "owner_register.html",
                {"formbasic": formbasic, "formowner": formowner},
            )

    dic = {"formbasic": RegisterForm, "formowner": OwnerForm}

    return render(request, "owner_register.html", context=dic)


def loginpage(request):
    message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        user = authenticate(request, username=email, password=password)
        print(user)
        print(type(user))
        if user is not None:
            login(request, user)
            return redirect("ohome")
        else:
            messages.info(request, "Email or Password is Incorrect")
    return render(request, "login.html", {})


@login_required(login_url="/login")
def ohome(request):
    return render(request, "ohome.html", {})


@login_required(login_url="/login")
def logoutpage(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/login")
def results(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        # preferences
        bed_num = form_data["bed_num"]
        min_price = form_data["min_price"]
        max_price = form_data["max_price"]
        gender = form_data["gender"]
        structure = form_data["structure"]
        meal_system = form_data["meal_system"]
        region = form_data["region"]
        students = form_data["students"]
        distance = form_data["distance"]

        print(
            bed_num,
            min_price,
            max_price,
            gender,
            structure,
            meal_system,
            region,
            students,
            distance,
        )

        room_list = Room.objects.filter(
            bed_num=bed_num,
            price__gte=min_price,
            price__lte=max_price,
            mess__gender=gender,
            mess__structure=structure,
            mess__meal_system=meal_system,
            mess__region=region,
            mess__students_num__lte=students,
            mess__distance__lte=distance,
        )
        print(model_to_dict(Room.objects.get(id=7)))
        print(model_to_dict(Mess.objects.get(id=3)))
        return render(request, "result.html", {"room_list": room_list})
    return render(request, "result.html", {"room_list": Room.objects.all()})
    # return HttpResponse("Form is not Post")


@login_required(login_url="/login")
def room_details(request, id):
    room = Room.objects.get(id=id)
    comments = Comment.objects.filter(room=room)
    return render(request, "details.html", {"room": room, "comments": comments})


def mess_details(request, id):
    return HttpResponse("mess details page")


def add_mess(request):
    pass


def add_room(request):
    pass
