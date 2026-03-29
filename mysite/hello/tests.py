from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Donor, Item, ItemRequest, UserProfile


class HomePageTests(TestCase):
    def test_home_page_renders_caretrack(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hello/index.html")
        self.assertContains(response, "Welcome to CareTrack")

    def test_home_page_uses_shared_navigation(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Available Inventory")
        self.assertContains(response, "Requested Items")
        self.assertContains(response, "Distributed Items")


class PageStructureTests(TestCase):
    def test_inventory_page_renders(self):
        response = self.client.get(reverse("available_inventory"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Available Inventory")


class ModelTests(TestCase):
    def test_item_request_defaults_to_pending(self):
        user = get_user_model().objects.create_user(
            username="survivor1",
            email="survivor@example.com",
            password="StrongPassword123",
        )
        donor = Donor.objects.create(name="Helpful Donor")
        item = Item.objects.create(name="Blanket", donor=donor)
        request = ItemRequest.objects.create(requester=user, item=item)

        self.assertEqual(request.status, ItemRequest.Status.PENDING)

    def test_user_profile_default_role_is_public(self):
        user = get_user_model().objects.create_user(
            username="newuser",
            email="newuser@example.com",
            password="StrongPassword123",
        )
        profile = UserProfile.objects.create(user=user)

        self.assertEqual(profile.role, UserProfile.Role.PUBLIC)
