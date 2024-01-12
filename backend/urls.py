from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from backend.account.controllers import account_controller


api = NinjaAPI()
api.add_router('account', account_controller)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('backend.home.urls')),
    path('api/', api.urls),
]
