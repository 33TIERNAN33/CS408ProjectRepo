from django.contrib import admin

from .models import Donor, Item, ItemRequest, Survivor, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_approved")
    list_filter = ("role", "is_approved")
    search_fields = ("user__username", "user__email")


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "anonymous")
    list_filter = ("anonymous",)
    search_fields = ("name", "email", "phone")


@admin.register(Survivor)
class SurvivorAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_info")
    search_fields = ("name", "contact_info")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "status", "storage_location", "donor", "assigned_to")
    list_filter = ("status", "category")
    search_fields = ("name", "description", "category", "storage_location")


@admin.register(ItemRequest)
class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ("item", "requester", "status", "request_date")
    list_filter = ("status",)
    search_fields = ("item__name", "requester__username", "requester__email")
