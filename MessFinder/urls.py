from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path
from MainApp import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.shome, name="shome"),
    path("home/<int:id>", views.home, name="home"),
    path("shome", views.shome, name="shome"),

    path("register", views.register, name="register"),
    path("register/student", views.StudentRegister, name="studentregister"),
    path("register/owner", views.OwnerRegister, name="ownerregister"),


    path("login", views.loginpage, name="login"),
    path("logout", views.logoutpage, name="logout"),
  
    path("ohome/<int:id>", views.ohome, name="ohome"),
    
    path("profile/<int:id>", views.profile, name="profile"),

    path("room/<int:id>", views.room_details, name="room_details"),
    path("update_room/<int:id>", views.update_room, name="update_room"),
    path("delete_room/<int:id>", views.delete_room, name="delete_room"),
    path("add_room/<int:id>", views.add_room, name="add_room"),
    path("comment", views.comment, name="comment"),
    
    path('add_mess/<int:id>', views.add_mess, name = 'add_mess'),
    path("mess/<int:id>", views.mess_details, name="mess_details"),
    path('all_mess', views.results, name='all_mess'),
    path("results", views.results, name="results"),
    path("review", views.review, name="review"),
    path('edit_mess/<int:id>', views.edit_mess, name = 'edit_mess'),
    path('delete_mess/<int:id>', views.delete_mess, name = 'delete_mess'),
    
    
    # path("sprofile/<int:sid>", views.sprofile, name = sprofile),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
