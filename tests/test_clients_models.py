from django.test import TestCase, SimpleTestCase
from apps.clients.models import Client, Invoice
from apps.customuser.models import CustomUser
import pytest


class TestClientsModels(TestCase):

    def setUp(self):
        self.client = Client.objects.create(psid="psid1", fname="rulo1", lname="sosi1", email="rulo@r.com")

    def test_client_models_01(self):
        assert self.client.fname == "rulo1"
