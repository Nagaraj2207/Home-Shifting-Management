from django.contrib import admin
from . models import User_Registration,Booking_detail

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["id","name","email","password","MoveEasePerson","delivery_person","contact"]
 
admin.site.register(User_Registration, RegistrationAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ["id","email","shifting_from","shifting_to","bhk_type","service_time","extra_cortans","selected_vehicle",
                    "bill_amount","deliver_status","payment_status","delivery_person"]
 
admin.site.register(Booking_detail, BookingAdmin)