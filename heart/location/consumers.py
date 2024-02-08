import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))
            return

        nickname = text_data_json.get('nickname')
        coordinates = text_data_json.get('coordinates')
        if not nickname or not coordinates:
            await self.send(text_data=json.dumps({'error': 'Missing nickname or coordinates'}))
            return

        longitude = float(coordinates.get('longitude'))
        latitude = float(coordinates.get('latitude'))
        if not longitude or not latitude:
            await self.send(text_data=json.dumps({'error': 'Missing longitude or latitude'}))
            return

        try:
            cache.client.get_client().geoadd("locations", (longitude, latitude, nickname))
        except Exception as e:
            await self.send(text_data=json.dumps({'error': f'Redis error {e}'}))
            return

        await self.send(text_data=json.dumps({'message': 'Location updated successfully'}))
