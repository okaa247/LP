from django.contrib import admin
from .models import *
from django.apps import AppConfig

# Register your models here.

@admin.register(UserRegistration)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_email_verified', 'phone_number', 'created_at')


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')


class RegistrationConfig(AppConfig):
    name = 'registration'

    def ready(self):
        from . import models  # Ensure the models (and signals) are loaded


@admin.register(National)
class NationalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'state', 'lga', 'ward', 'membership_status', 'created_at', 'updated_at')
    
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'ward', 'created_at', 'updated_at')











# @admin.register(WardMembership)
# class WardMembershipAdmin(admin.ModelAdmin):
#     list_display = ('user', 'ward', 'status', 'created_at', 'updated_at')

# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('role_name', 'created_at', 'updated_at')

# @admin.register(UserRole)
# class UserRoleAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role', 'level', 'level_id', 'created_at', 'updated_at')

# @admin.register(PollingUnit)
# class PollingUnitAdmin(admin.ModelAdmin):
#     list_display = ('name', 'ward', 'created_at', 'updated_at')

# @admin.register(PollingUnitAgent)
# class PollingUnitAgentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'polling_unit', 'ward', 'created_at', 'updated_at')
