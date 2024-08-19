# myapp/tests.py
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.urls import reverse
from dashboard.routing import application

class DashboardConsumerTest(TestCase):
    async def test_dashboard_consumer(self):
        communicator = WebsocketCommunicator(application, "/ws/dashboard/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        response = await communicator.receive_json_from()
        self.assertIsInstance(response, dict)
        
        await communicator.disconnect()
