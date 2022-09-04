from django.contrib import admin

from django.urls import path
from api.views import get_route, get_all_name_routes


urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:type_transport>/route/name_all/', get_all_name_routes, name='get_all_routes_name'),
    path('<str:type_transport>/route/<str:number>/', get_route, name='get_route')
]
