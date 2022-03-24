from django.http import HttpResponse
from django.shortcuts import redirect, render

from MainApp.models import *

from .forms import *


def index(request):

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
        print(request.POST)
        if formbasic.is_valid():
            form_b = formbasic.save(commit=False)
            form_b.is_student = False
            print("-------Printing form_b--------")
            print(type(form_b))
            form_b.save()
            print(formbasic.cleaned_data.get("email"))

            # print(type(form_b))
        else:
            print("basic invalid")
            for field in formbasic:
                for error in field.errors:
                    print(error)
        print("..........Custom User Obejct........")
        print(
            CustomUser.objects.filter(email=formbasic.cleaned_data.get("email")).first()
        )

        if formowner.is_valid():
            form_o = formowner.save(commit=False)

            form_o.user = form_b
            form_o.save()
            print("form owner successfully saved")
        else:
            print("owner invalid")
            for field in formowner:
                for error in field.errors:
                    print(error)

        return render(
            request,
            "owner_register.html",
            {"formbasic": formbasic, "formowner": formowner},
        )

    dic = {"formbasic": RegisterForm, "formowner": OwnerForm}

    return render(request, "owner_register.html", context=dic)


def login(request):
    # if request.method == "POST":

    return render(request, "login.html", {})


def results(request):
    result = Room.objects.all()

    return render(request, "result.html", {"result": result})
