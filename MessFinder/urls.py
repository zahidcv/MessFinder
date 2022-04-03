from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path
from MainApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.shome, name="shome"),
    path("shome", views.shome, name="shome"),
    path("register", views.register, name="register"),
    path("register/student", views.StudentRegister, name="studentregister"),
    path("register/owner", views.OwnerRegister, name="ownerregister"),
    path("login", views.loginpage, name="login"),
    path("results", views.results, name="results"),
    path("logout", views.logoutpage, name="logout"),
    path("ohome/<int:id>", views.ohome, name="ohome"),
    path("room/<int:id>", views.room_details, name="room_details"),
    path("mess/<int:id>", views.mess_details, name="mess_details"),
    path("update_room/<int:id>", views.update_room, name="update_room"),
    path("delete_room/<int:id>", views.delete_room, name="delete_room"),
    path("add_room/<int:id>", views.add_room, name="add_room"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
