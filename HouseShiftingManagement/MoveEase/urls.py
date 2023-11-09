"""
URL configuration for HouseShiftingManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("register/",views.user_registration,name="register"),
    path("login/",views.user_login,name="login"),
    path("login/forgot_password/",views.forget_pass,name="forgot_password"),
    path("login/verify_login/",views.verify_login,name="verify_login"),
    path("login/customer/",views.customer,name="customer_app"),
    path("login/customer/free_quote/",views.free_qoute,name="free_quote"),
    path("login/customer/free_quote/send_qoute/",views.send_quotation,name="send_qoute"),
    path("login/customer/my_booking/",views.my_booking,name="my_booking"),
    path("login/customer/my_booking/delete_booking_detail/",views.delete_booking_detail,name="delete_booking_detail"),
    path("login/customer/profile_setting/",views.user_profile,name="profile_setting"),
    path("login/customer/profile_setting/update_user/",views.update_user,name="update_user"),
    path("login/customer/profile_setting/change_password/",views.change_password,name="change_password"),
    path("login/customer/map/",views.map,name="map"),
    path("login/customer/inventry/",views.inventry,name="inventry"),
    path("login/customer/inventry/payment_receipts/",views.payment_receipts,name="payment_receipts"),
    path("login/customer/inventry/payment/",views.payment,name="payment"),
    path("login/customer/inventry/payment/save_bookings/",views.save_bookings,name="save_bookings"),
    path("move_ease_app/",views.move_ease_app,name="move_ease_app"),
    path("move_ease_app/add_delivery_person/",views.add_delivery_person,name="add_delivery_person"),
    path("move_ease_app/update_booking_detail/",views.update_booking_detail,name="update_booking_detail"),
    path("delivery_app/",views.delivery_person_app,name="delivery_app"),
]
