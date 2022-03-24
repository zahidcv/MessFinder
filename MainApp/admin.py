from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password','name','is_student','number', 'profile_pic', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'name','is_student','number', 'profile_pic')
            }
        ),
    )

    list_display = ('email', 'name', 'is_staff', 'is_student')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class RoomImagesAdmin(admin.StackedInline):
    model = RoomImages

class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImagesAdmin]

class MessImagesAdmin(admin.StackedInline):
    model = MessImages

class MessAdmin(admin.ModelAdmin):
    inlines = [MessImagesAdmin]


admin.site.register(CustomUser, UserAdmin)

admin.site.register(Owner)
admin.site.register(Student)
admin.site.register(Mess, MessAdmin)
admin.site.register(Room, RoomAdmin)
