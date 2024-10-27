from django.test import TestCase, Client
from django.urls import reverse
from search.models import Restaurant
from django.contrib.auth.models import User
import uuid
import json

class SearchViewTest(TestCase):
    def setUp(self):
        # Set up test client
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # Create test restaurants
        self.restaurant1 = Restaurant.objects.create(
            nama='Warung Tegal',
            jenis_makanan='indonesia',
            rating=4.5,
            harga=25000,
            jarak=1.5,
            suasana='Santai',
            entertainment=3,
            keramaian=2
        )
        
        self.restaurant2 = Restaurant.objects.create(
            nama='Burger King',
            jenis_makanan='western',
            rating=3.5,
            harga=50000,
            jarak=2.5,
            suasana='Modern',
            entertainment=4,
            keramaian=4
        )

    def test_show_search_get(self):
        """Test basic search page load"""
        response = self.client.get(reverse('search:show_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_ajax_search_no_filters(self):
        """Test AJAX search without filters"""
        response = self.client.get(
            reverse('search:show_search'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('html' in json.loads(response.content))

    def test_ajax_search_with_name(self):
        """Test AJAX search with name filter"""
        response = self.client.get(
            reverse('search:show_search'),
            {'nama': 'Warung'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('Warung Tegal', content['html'])

    def test_ajax_search_with_food_type(self):
        """Test AJAX search with food type filter"""
        response = self.client.get(
            reverse('search:show_search'),
            {'jenis_makanan': 'western'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('Burger King', content['html'])

    def test_ajax_search_with_rating(self):
        """Test AJAX search with rating filter"""
        response = self.client.get(
            reverse('search:show_search'),
            {'rating': '4'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('Warung Tegal', content['html'])

    def test_ajax_search_with_sorting(self):
        """Test AJAX search with sorting"""
        response = self.client.get(
            reverse('search:show_search'),
            {'sort_by': '-rating'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

    def test_ajax_search_no_results(self):
        """Test AJAX search with no results"""
        response = self.client.get(
            reverse('search:show_search'),
            {'nama': 'NonexistentRestaurant'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('Tidak ada data yang cocok', content['html'])

    def test_show_xml(self):
        """Test XML endpoint"""
        response = self.client.get(reverse('search:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        """Test JSON endpoint"""
        response = self.client.get(reverse('search:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        """Test XML by ID endpoint"""
        response = self.client.get(
            reverse('search:show_xml_by_id', args=[str(self.restaurant1.id)])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id(self):
        """Test JSON by ID endpoint"""
        response = self.client.get(
            reverse('search:show_json_by_id', args=[str(self.restaurant1.id)])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_authenticated_user_view(self):
        """Test view for authenticated user"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(
            reverse('search:show_search'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('Suasana', content['html'])

    def test_unauthenticated_user_view(self):
        """Test view for unauthenticated user"""
        response = self.client.get(
            reverse('search:show_search'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertNotIn('Suasana', content['html'])

    def test_all_rating_filters(self):
        """Test all rating filter options"""
        rating_options = ['0', '1', '2', '3', '4']
        for rating in rating_options:
            response = self.client.get(
                reverse('search:show_search'),
                {'rating': rating},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEqual(response.status_code, 200)

    def test_model_str_method(self):
        """Test Restaurant model string representation"""
        expected_str = f"{self.restaurant1.nama} {self.restaurant1.jenis_makanan} {self.restaurant1.rating} {self.restaurant1.harga} {self.restaurant1.jarak} {self.restaurant1.suasana} {self.restaurant1.entertainment} {self.restaurant1.keramaian}"
        self.assertEqual(str(self.restaurant1), expected_str)

    # Tambahkan test case berikut ke dalam class SearchViewTest

    def test_multiple_filter_combination(self):
        """Test search with multiple filters combined"""
        response = self.client.get(
            reverse('search:show_search'),
            {
                'nama': 'Warung',
                'jenis_makanan': 'indonesia',
                'rating': '4',
                'sort_by': '-harga'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('Warung', content['html'])

    def test_invalid_sort_parameter(self):
        """Test search with invalid sort parameter"""
        response = self.client.get(
            reverse('search:show_search'),
            {'sort_by': 'invalid_sort'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

    def test_empty_search_parameters(self):
        """Test search with empty parameters"""
        response = self.client.get(
            reverse('search:show_search'),
            {'nama': '', 'jenis_makanan': '', 'rating': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

    def test_non_ajax_request_with_parameters(self):
        """Test non-AJAX request with search parameters"""
        response = self.client.get(
            reverse('search:show_search'),
            {'nama': 'Warung', 'jenis_makanan': 'indonesia'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

   