# Create your tests here.

from django.test import TestCase, Client
from django.urls import reverse
from .models import Makanan
from .forms import MakananUpdateForm, PreferensiForm
from django.contrib.auth.models import User

class MakananViewTestsUser(TestCase):
    def setUp(self):
        # Setup untuk user login dan data dummy Makanan
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.makanan1 = Makanan.objects.create(preferensi="Indonesia", menu="Nasi Goreng", restoran="Restoran Nusantara")
        self.makanan2 = Makanan.objects.create(preferensi="Italia", menu="Pasta", restoran="Restoran Italia")
    
    def test_makanan_list_view(self):
        # Test halaman makanan_list menampilkan daftar makanan
        response = self.client.get(reverse('tipemakanan:makanan_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'makanan_list.html')
        self.assertContains(response, "Daftar Tipe Makanan Berdasarkan Preferensi Negara")

    def test_makanan_list_filter(self):
        # Test filter preferensi negara pada makanan_list
        response = self.client.post(reverse('tipemakanan:makanan_list'), {'preferensi': 'Indonesia'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.makanan1.menu)
        self.assertNotContains(response, self.makanan2.menu)
    
    def test_edit_makanan_get(self):
        # Test akses GET untuk edit_makanan dengan modal AJAX
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('tipemakanan:edit_makanan', args=[self.makanan1.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form_html', response.json())
        self.assertIn("Nasi Goreng", response.json()['form_html'])  # Memeriksa apakah form menampilkan makanan yang benar

    def test_edit_makanan_post(self):
        # Test penyimpanan perubahan pada form AJAX edit_makanan
        self.client.login(username='testuser', password='password')
        new_data = {
            'preferensi': 'Indonesia',
            'menu': 'Mie Goreng',
            'restoran': 'Restoran Nusantara'
        }
        response = self.client.post(reverse('tipemakanan:edit_makanan', args=[self.makanan1.pk]), data=new_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)

        # Memastikan data telah diperbarui dalam database
        self.makanan1.refresh_from_db()
        self.assertEqual(self.makanan1.menu, 'Mie Goreng')


class MakananModelTests(TestCase):
    def setUp(self):
        self.makanan = Makanan.objects.create(
            preferensi="Indonesia",
            menu="Nasi Goreng",
            restoran="Warung Nusantara"
        )

    def test_makanan_str_method(self):
        self.assertEqual(
            str(self.makanan),
            "Warung Nusantara - Indonesia: Nasi Goreng"
        )

class MakananViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.makanan = Makanan.objects.create(
            preferensi="Indonesia",
            menu="Sate Ayam",
            restoran="Warung Sate"
        )

    def test_makanan_list_view_get(self):
        response = self.client.get(reverse('tipemakanan:makanan_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'makanan_list.html')
        self.assertContains(response, "Daftar Tipe Makanan Berdasarkan Preferensi Negara")

    def test_makanan_list_view_post_with_filter(self):
        response = self.client.post(reverse('tipemakanan:makanan_list'), data={'preferensi': 'Indonesia'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Warung Sate')
        self.assertContains(response, 'Sate Ayam')

    def test_edit_makanan_view_get(self):
        # Simulate AJAX GET request for edit modal
        response = self.client.get(reverse('tipemakanan:edit_makanan', args=[self.makanan.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form_html', response.json())
        self.assertIn('Sate Ayam', response.json()['form_html'])

    def test_edit_makanan_view_post_success(self):
        # Simulate AJAX POST request to save changes
        response = self.client.post(
            reverse('tipemakanan:edit_makanan', args=[self.makanan.pk]),
            data={'preferensi': 'Indonesia', 'menu': 'Sate Kambing', 'restoran': 'Warung Sate'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.makanan.refresh_from_db()
        self.assertEqual(self.makanan.menu, 'Sate Kambing')

class MakananFormTests(TestCase):
    def test_makanan_update_form_valid(self):
        makanan = Makanan.objects.create(
            preferensi="Jepang",
            menu="Sushi",
            restoran="Tokyo Dine"
        )
        form_data = {
            'preferensi': makanan.preferensi,
            'menu': "Sashimi",
            'restoran': makanan.restoran
        }
        form = MakananUpdateForm(data=form_data, instance=makanan)
        self.assertTrue(form.is_valid())

    def test_preferensi_form_choices(self):
        # Ensuring unique preferences are included in the form
        Makanan.objects.create(preferensi="China", menu="Dimsum", restoran="Dragon Palace")
        form = PreferensiForm()
        self.assertIn(('China', 'China'), form.fields['preferensi'].choices)
