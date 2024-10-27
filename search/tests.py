from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from search.models import Restaurant
from django.http import JsonResponse
import json

class RestaurantSearchTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create sample restaurants
        self.restaurant1 = Restaurant.objects.create(
            nama="Warung Pak Eko",
            jenis_makanan="indonesia",
            rating=4.5,
            harga=25000,
            jarak=1.5,
            suasana="Nyaman",
            entertainment=3,
            keramaian=2
        )

        self.restaurant2 = Restaurant.objects.create(
            nama="Western Grill",
            jenis_makanan="western",
            rating=3.5,
            harga=75000,
            jarak=2.0,
            suasana="Modern",
            entertainment=4,
            keramaian=3
        )

        self.restaurant3 = Restaurant.objects.create(
            nama="Sushi Place",
            jenis_makanan="japanese",
            rating=4.8,
            harga=100000,
            jarak=3.0,
            suasana="Elegant",
            entertainment=5,
            keramaian=4
        )

    def test_show_search_page(self):
        """Test that search page loads correctly"""
        response = self.client.get(reverse('search:show_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_ajax_search_by_name(self):
        """Test AJAX search by restaurant name"""
        response = self.client.get(
            reverse('search:show_search'),
            {'nama': 'Warung'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, JsonResponse))
        self.assertIn('Warung Pak Eko', response.content.decode())

    def test_search_by_food_type(self):
        """Test search filtering by food type"""
        response = self.client.get(
            reverse('search:show_search'),
            {'jenis_makanan': 'japanese'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sushi Place', response.content.decode())

    def test_search_by_rating_ranges(self):
        """Test search filtering by different rating ranges"""
        rating_ranges = ['0', '1', '2', '3', '4']
        for rating in rating_ranges:
            response = self.client.get(
                reverse('search:show_search'),
                {'rating': rating},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEqual(response.status_code, 200)

    def test_sort_results(self):
        """Test sorting functionality"""
        sort_options = ['nama', '-nama', 'rating', '-rating', 'harga', '-harga', 'jarak', '-jarak']
        for sort_by in sort_options:
            response = self.client.get(
                reverse('search:show_search'),
                {'sort_by': sort_by},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEqual(response.status_code, 200)

    def test_no_results_found(self):
        """Test when no results match search criteria"""
        response = self.client.get(
            reverse('search:show_search'),
            {'nama': 'NonExistentRestaurant'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tidak ada data yang cocok', response.content.decode())

    def test_multiple_search_criteria(self):
        """Test searching with multiple criteria"""
        response = self.client.get(
            reverse('search:show_search'),
            {
                'nama': 'Warung',
                'jenis_makanan': 'indonesia',
                'rating': '4'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

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
        response = self.client.get(reverse('search:show_xml_by_id', args=[self.restaurant1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id(self):
        """Test JSON by ID endpoint"""
        response = self.client.get(reverse('search:show_json_by_id', args=[self.restaurant1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_model_str_method(self):
        """Test the string representation of Restaurant model"""
        expected_str = f"{self.restaurant1.nama} {self.restaurant1.jenis_makanan} {self.restaurant1.rating} {self.restaurant1.harga} {self.restaurant1.jarak} {self.restaurant1.suasana} {self.restaurant1.entertainment} {self.restaurant1.keramaian}"
        self.assertEqual(str(self.restaurant1), expected_str)

    def test_authenticated_user_view(self):
        """Test view differences for authenticated users"""
        # Test without authentication
        response = self.client.get(reverse('search:show_search'))
        self.assertEqual(response.status_code, 200)
        
        # Test with authentication
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('search:show_search'))
        self.assertEqual(response.status_code, 200)
