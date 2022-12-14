from django.contrib import admin

from django.urls import path
from api.views import get_route, get_all_name_routes, get_route_from_stops, get_nearest_route


urlpatterns = [
    path('admin/', admin.site.urls),
    path('route/<str:type_transport>/name_all/', get_all_name_routes, name='get_all_routes_name'),
    path('route/<str:type_transport>/<str:number>/', get_route, name='get_route'),
    path('route/routes_from_stops/', get_route_from_stops, name='get_route_with_stops'),
    path('route/nearest_route/', get_nearest_route, name='get_nearest_route')
]
