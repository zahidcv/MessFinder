from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path
from MainApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("shome", views.shome, name="shome"),
    path("register", views.register, name="register"),
    path("register/student", views.StudentRegister, name="studentregister"),
    path("register/owner", views.OwnerRegister, name="ownerregister"),
    # path('register/teacher',views.OwnerRegister, name = 'ownerregister'),
    path("login", views.loginpage, name="login"),
    path("results", views.results, name="result"),
    path("logout", views.logoutpage, name="logout"),
    path("ohome", views.ohome, name="ohome"),
    path("details/<int:id>", views.details, name="details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
