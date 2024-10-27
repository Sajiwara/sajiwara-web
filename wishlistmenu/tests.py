# wishlistmenu/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from wishlistmenu.models import Menu, Restaurant, WishlistMenu
from wishlistmenu.forms import WishlistMenuForm
from django.contrib.auth.models import User

class WishlistMenuTests(TestCase):
    def setUp(self):
        # Setup data yang digunakan di semua test
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.restaurant = Restaurant.objects.create(name="Test Resto")
        self.menu = Menu.objects.create(menu="Test Menu", restaurant=self.restaurant)
        self.client.login(username='testuser', password='testpass')

    # Test Model
    def test_menu_creation(self):
        # Test untuk memastikan objek Menu dibuat dengan benar
        self.assertEqual(self.menu.menu, "Test Menu")
        self.assertEqual(self.menu.restaurant.name, "Test Resto")

    # Test View: show_wishlistmenu
    def test_show_wishlistmenu_view(self):
        # Test untuk memastikan view show_wishlistmenu berfungsi dengan benar
        response = self.client.get(reverse('wishlistmenu:show_wishlistmenu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_wishlistmenu.html')

    def test_add_to_wishlistmenu_view(self):
        response = self.client.post(
            reverse('wishlistmenu:add_to_wishlistmenu'), 
            {'menu': self.menu.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # Simulate AJAX request
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {'success': True, 'message': 'Menu berhasil ditambahkan ke wishlist!'}
        )
    # Test Form: WishlistMenuForm
    def test_wishlist_form_valid(self):
        # Test untuk validasi form yang benar
        form = WishlistMenuForm(data={'menu': self.menu.id})
        self.assertTrue(form.is_valid())

    def test_wishlist_form_invalid(self):
        # Test untuk form yang tidak valid (data kosong)
        form = WishlistMenuForm(data={})  
        self.assertFalse(form.is_valid())
