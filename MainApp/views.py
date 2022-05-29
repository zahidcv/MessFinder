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


def home(request, id):
    if request.user.is_superuser:
        print('You are a SuperUser, what are you doint here? ')
        return redirect('login')

    if request.user.is_student:
        return redirect('shome')
    else:
        return redirect('ohome', id = request.user.id)

@login_required(login_url="/login")
def shome(request):

    return render(request, "shome.html", {})


@login_required(login_url="/login")
def ohome(request, id):
    # print("id", id)

    user = CustomUser.objects.get(id=id)
    if user.is_student:
        return redirect("shome")
    if user.is_superuser:
        return HttpResponse("You are a SuperUser, what are you doint here? ")
    print("user", user)
    # print("user.is_student", user.is_student)
    owner = Owner.objects.get(user=user)
    print("owner", type(owner))
    messes = Mess.objects.filter(owner=owner)
    # print("mess", mess)
    # rooms = Rooms.objects.filter(mess=messes)
    # rooms  = []
    # for mess in messes:
    #     rooms.append(Room.objects.filter(mess=mess))
    # rooms = {}
    # for mess in messes:
    #     rooms[mess] = Room.objects.filter(mess = mess)

    rooms = Room.objects.filter(mess__in = messes.values_list('id'))
    print('|'*10)
    for room in rooms:
        print(room)
    return render(
        request,
        "ohome.html",
        {
            "owner": owner,
            "messes": messes,
            "rooms": rooms,
        },
    )

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
            print("User Id:", user.id)
            login(request, user)
            if user.is_student:
                return redirect("shome")
            else:
                return redirect("ohome/" + str(user.id))
        else:
            messages.info(request, "Email or Password is Incorrect")
    return render(request, "login.html", {})





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
        # print(model_to_dict(Room.objects.get(id=7)))
        # print(model_to_dict(Mess.objects.get(id=3)))
        return render(request, "result.html", {"room_list": room_list})
    return render(request, "result.html", {"room_list": Room.objects.all()})
    # return HttpResponse("Form is not Post")


@login_required(login_url="/login")
def room_details(request, id):
    room = Room.objects.get(id=id)
    comments = Comment.objects.filter(room=room)
    return render(request, "room_details.html", {"room": room, "comments": comments})



def add_mess(request, id):
    user = CustomUser.objects.get(id=id)
    
    if user.is_student:                     #checing id the requesting person is user or owner
        return redirect("shome")

    messform = MessForm()

    if request.method == 'POST':
        form = MessForm(request.POST, request.FILES)

        if form.is_valid():
            mess = form.save(commit=False)
            owner = Owner.objects.get(user = user)
            mess.owner = owner

            print("............")
            print(mess)
            mess.save()

            return redirect("ohome", id=id)


        else:
            print("form is invalid")
            for error in form.errors:
                print(error)
    return render(request, 'add_mess.html', {'messform': messform})


    


def profile(request, id):

    user = CustomUser.objects.get(id = id)
    print(f"printing user.id---->{user.id}")
    if user != request.user:
        if request.user.is_student:
            return redirect('shome')
        else:
            return redirect('ohome', id = request.user.id)
    # print(user)
    if user.is_superuser or user.is_staff:
        return HttpResponse("You are SuperUser, Didn't expect you here!")
    if user is not None:
        if user.is_student:
            student = Student.objects.get(user = user)
            return render(request,'sprofile.html', {'student': student })
        else:
            owner  = Owner.objects.get(user = user)
            return redirect("ohome", id = owner.id)
    else:
        return HttpResponse("Profile Not found")

# def sprofile(request, sid):



def mess_details(request, id):
    mess = Mess.objects.get(id=id)
    rooms = Room.objects.filter(mess=mess)
    reviews = Review.objects.filter(mess = mess)
    return render(request, "mess_details.html", {"mess": mess, "rooms": rooms, "reviews": reviews})


@login_required(login_url="/login")
def update_room(request, id):
    if request.user.id != id:
        return redirect("shome")
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("room_details", id=id)
        else:
            print("form is invalid")
            for error in form.errors:
                print(error)

    return render(request, "update_room.html", {"form": form, "room": room})
    # return HttpResponse("update room")


@login_required(login_url="/login")
def delete_room(request, id):
    room = Room.objects.get(id = id)

    if request.user != room.mess.owner.user:
        return redirect("shome")

    
    
    print('deleting room', room)
    room.delete()

    return redirect("ohome", id = request.user.id)

def delete_mess(request,id):
    mess = Mess.objects.get(id = id)
    if request.user != mess.owner.user:
        return redirect("shome")

    mess = Mess.objects.get(id = id)
    print('deleting mess', mess)
    mess.delete()
    return redirect("ohome", id = request.user.id)

@login_required(login_url="/login")
def add_room(request, id):
    mess = Mess.objects.get(id=id)
    print(".........mess....", mess)
    # print(mess)
    form = RoomForm(initial={"mess": mess, "owner": mess.owner})
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        room = form.save(commit=False)
        print(type(room))
        room.mess = mess
        room.owner = mess.owner
        print("............")
        print(room)
        if form.is_valid():
            form.save()
            return redirect("mess_details", id=id)
        else:
            print("form is invalid")
            for error in form.errors:
                print(error)
    return render(request, "add_room.html", {"form": form})



@login_required(login_url='login')
def comment(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")

        comment = request.POST.get("comment")

        room = Room.objects.get(id=room_id)
      
        comment = Comment(content=comment, room=room, commenter = request.user)
        comment.save()
        return redirect("room_details", id=room_id)
    return render(request, "view_product.html", {'room': room})


@login_required(login_url='login')
def review(request):
    
    if request.method == "POST":
        mess_id = request.POST.get("mess_id")
        mess = Mess.objects.get(id=mess_id)

        content = request.POST.get("content")

        #* reviewer and owner is the same person
        if request.user == mess.owner.user or request.user.is_superuser:
            rooms = Room.objects.filter(mess=mess)
            return render(request, "mess_details.html", {"mess": mess, "rooms": rooms})
        
      
        review = Review(content=content, mess=mess, reviewer = request.user)
        review.save()
        return redirect("mess_details", id=mess_id)

    rooms = Room.objects.filter(mess=mess)
    return render(request, "mess_details.html", {"mess": mess, "rooms": rooms})


@login_required(login_url='login')
def edit_mess(request,id):
    mess = Mess.objects.get(id = id)
    messform = MessForm(instance=mess)
    # print(mess)
    if request.method == "POST":
        form = MessForm(request.POST, instance=mess)
        if form.is_valid():
            form.save()
            return redirect("ohome", id=mess.owner.user.id)
        else:
            print("form is invalid")
            for error in form.errors:
                print(error)
    return render(request, 'edit_mess.html', {'messform': messform, 'mess':mess})
