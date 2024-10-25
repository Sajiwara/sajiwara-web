from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Resto, WishlistResto

User = get_user_model()

class WishlistRestoTests(TestCase):

    def setUp(self):
        # Membuat pengguna untuk pengujian
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Membuat contoh restoran
        self.resto1 = Resto.objects.create(restaurant='Restoran A')
        self.resto2 = Resto.objects.create(restaurant='Restoran B')

        # Menambahkan restoran ke wishlist
        self.wishlist_entry = WishlistResto.objects.create(
            restaurant_wanted=self.resto1.restaurant,
            user=self.user,
            wanted_resto=True
        )

    def test_show_wishlistresto(self):
        # Mengakses halaman wishlist
        response = self.client.get(reverse('wishlistresto:show_wishlistresto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_wishlistresto.html')
        self.assertContains(response, 'Daftar Wishlist Restoran')
        self.assertContains(response, 'Restoran A')

    def test_add_to_wishlist(self):
        # Menguji penambahan restoran ke wishlist
        response = self.client.post(reverse('wishlistresto:add_to_wishlist'), {
            'restaurant': self.resto2.pk
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'message': 'Restoran berhasil ditambahkan ke wishlist!',
            'restaurant': 'Restoran B'
        })
        self.assertEqual(WishlistResto.objects.count(), 2)

    def test_delete_wishlist(self):
        # Menguji penghapusan wishlist
        response = self.client.post(reverse('wishlistresto:delete_wishlist', args=[self.wishlist_entry.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertEqual(WishlistResto.objects.count(), 0)

    def test_mark_as_visited(self):
        # Menguji menandai restoran sebagai dikunjungi
        response = self.client.post(reverse('wishlistresto:visited_resto', args=[self.wishlist_entry.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.wishlist_entry.refresh_from_db()
        self.assertTrue(self.wishlist_entry.visited)

    def test_mark_as_not_visited(self):
        # Menguji menandai restoran sebagai tidak dikunjungi
        self.wishlist_entry.visited = True
        self.wishlist_entry.save()
        
        response = self.client.post(reverse('wishlistresto:not_visited_resto', args=[self.wishlist_entry.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.wishlist_entry.refresh_from_db()
        self.assertFalse(self.wishlist_entry.visited)
