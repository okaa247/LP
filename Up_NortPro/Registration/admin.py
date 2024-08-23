from django.contrib import admin
from .models import *
from django.apps import AppConfig

# Register your models here.

@admin.register(UserRegistration)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_email_verified', 'membership_id', 'phone_number', 'created_at')

class RegistrationConfig(AppConfig):
    name = 'registration'

    def ready(self):
        from . import models  



@admin.register(PollingUnit)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter_registered', 'created_at')

@admin.register(WardMembership)
class WardAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'ward', 'membership_id', 'created_at',)




@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)

@admin.register(LGAMembership)
class LGAAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'lga', 'created_at', 'updated_at')




@admin.register(MyState)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(StateMembership)
class StateAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'state', 'created_at')    



@admin.register(National)
class NationalAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(NationalMembership)
class NationalAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', )


@admin.register(PollingUnitAgent)
class PollingUnitAgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'polling_unit', 'ward', 'agent_status', 'created_at')








# @admin.register(PollingUnit)
# class PollingUnitAdmin(admin.ModelAdmin):
#     list_display = ('name', 'ward', 'created_at', 'updated_at')


