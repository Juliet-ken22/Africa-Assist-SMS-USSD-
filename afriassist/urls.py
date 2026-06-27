from django.contrib import admin
from django.urls import path
from api.views import sms_reply, ussd_reply, dashboard, api_messages

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/', sms_reply, name='sms_reply'),
    path('ussd/', ussd_reply, name='ussd_reply'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/messages/', api_messages, name='api_messages'),
]