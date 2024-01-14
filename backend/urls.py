from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from backend.account.controllers import account_controller
from backend.party.controllers import party_controller
from backend.video.controllers import video_controller


api = NinjaAPI()
api.add_router('account', account_controller)
api.add_router('party', party_controller)
api.add_router('video', video_controller)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('backend.home.urls')),
    path('api/', api.urls),
    path('party/', include('backend.party.urls')),
]
