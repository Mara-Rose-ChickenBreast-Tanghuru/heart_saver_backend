from django.urls import path

from location import consumers

websocket_urlpatterns = [
    path('ws/location/', consumers.LocationConsumer.as_asgi()),
]