from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

# Register your models here.


class OwnerAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


# class StudentAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',)
# class OwnerAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',)
# class OwnerAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "name",
                    "is_student",
                    "number",
                    "profile_pic",
                    "last_login",
                    
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_student",
                    "number",
                    "profile_pic",
                ),
            },
        ),
    )

    list_display = ("email", "name", "is_superuser", "is_student", "id")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


# class RoomImagesAdmin(admin.StackedInline):
#     model = RoomImages

# class RoomAdmin(admin.ModelAdmin):
#     inlines = [RoomImagesAdmin]

# class MessImagesAdmin(admin.StackedInline):
#     model = MessImages

# class MessAdmin(admin.ModelAdmin):
#     inlines = [MessImagesAdmin]


admin.site.register(CustomUser, UserAdmin)

admin.site.register(Owner, OwnerAdmin)
admin.site.register(Student)
admin.site.register(Mess)
admin.site.register(Room)
admin.site.register(Comment)
admin.site.register(Review)
