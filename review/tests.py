from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restor, Review
from .forms import ReviewForm
import json
import uuid

class ReviewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a test restaurant with UUID
        self.restaurant = Restor.objects.create(
            id=uuid.uuid4(),
            restaurant='Test Restaurant',
            rating=4.5
        )
        
        # Create a client for making requests
        self.client = Client()
    
    def test_show_main(self):
        """Test the main page view"""
        response = self.client.get(reverse('review:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_main.html')
        self.assertIn('restaurants', response.context)
    
    def test_restaurant_detail(self):
        """Test the restaurant detail view"""
        response = self.client.get(
            reverse('review:restaurant_detail', 
            args=[str(self.restaurant.id)])  # Convert UUID to string
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_detail.html')
        self.assertEqual(response.context['restaurant'], self.restaurant)
    
    def test_add_review_unauthorized(self):
        """Test adding review without authentication"""
        response = self.client.post(
            reverse('review:add_review', args=[str(self.restaurant.id)]),
            {'review': 'Great place!'},
        )
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Login required')
    
    def test_add_review_authorized(self):
        """Test adding review with authentication"""
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('review:add_review', args=[str(self.restaurant.id)]),
            {'review': 'Great place!'},
        )
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        
        # Verify review was created
        self.assertTrue(Review.objects.filter(
            user=self.user,
            restaurant=self.restaurant
        ).exists())
    
    def test_edit_review(self):
        """Test editing a review"""
        # Create a review
        review = Review.objects.create(
            id=uuid.uuid4(),
            user=self.user,
            restaurant=self.restaurant,
            review='Good place'
        )
        
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Edit the review
        response = self.client.post(
            reverse('review:edit_review', args=[str(review.id)]),
            {'review': 'Great place!'},
        )
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        
        # Verify review was updated
        updated_review = Review.objects.get(id=review.id)
        self.assertEqual(updated_review.review, 'Great place!')
    
    def test_delete_review(self):
        """Test deleting a review"""
        # Create a review
        review = Review.objects.create(
            id=uuid.uuid4(),
            user=self.user,
            restaurant=self.restaurant,
            review='Good place'
        )
        
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Delete the review
        response = self.client.post(
            reverse('review:delete_review', args=[str(review.id)])
        )
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        
        # Verify review was deleted
        self.assertFalse(Review.objects.filter(id=review.id).exists())

class RestorModelTests(TestCase):
    def test_restaurant_creation(self):
        """Test restaurant model"""
        restaurant = Restor.objects.create(
            id=uuid.uuid4(),
            restaurant='Test Restaurant',
            rating=4.5
        )
        self.assertEqual(restaurant.restaurant, 'Test Restaurant')
        self.assertEqual(restaurant.rating, 4.5)
        self.assertEqual(str(restaurant), 'Test Restaurant, 4.5')

class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.restaurant = Restor.objects.create(
            id=uuid.uuid4(),
            restaurant='Test Restaurant',
            rating=4.5
        )
    
    def test_review_creation(self):
        """Test review model"""
        review = Review.objects.create(
            id=uuid.uuid4(),
            user=self.user,
            restaurant=self.restaurant,
            review='Excellent place!'
        )
        self.assertEqual(review.review, 'Excellent place!')
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.restaurant, self.restaurant)
        self.assertTrue(str(review).startswith('Review by testuser on'))

class ReviewFormTests(TestCase):
    def test_review_form_valid(self):
        """Test review form with valid data"""
        form_data = {
            'review': 'Great place!'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid(self):
        """Test review form with invalid data"""
        form_data = {
            'review': ''  # Empty review
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())