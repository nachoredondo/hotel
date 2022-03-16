from django.contrib import admin
from buscadorReservas.models import Room, Reservation

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display= ("name", "capacity", "price")
    list_filter= ("capacity", "price")

class ReservationAdmin(admin.ModelAdmin):
    list_display= ("entry_date", "departure_date", "name", "phone_number")
    list_filter= ("entry_date", "departure_date")
    search_fields= ("name",)
    date_hierarchy = ("entry_date")


admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
