from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Restor
from .models import Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import ReviewForm, SearchForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q

# Create your views here.

def show_main(request):
    # Inisialisasi form pencarian dan form review
    search_form = SearchForm(request.GET or None)
    query = search_form.cleaned_data.get('query') if search_form.is_valid() else None

    # Jika ada query, filter restoran berdasarkan query
    if query:
        restaurants = Restor.objects.filter(Q(restaurant__icontains=query))
    else:
        restaurants = Restor.objects.all()

    # Inisialisasi form review
    review_form = ReviewForm()  

    # Mengatur konteks untuk dikirim ke template
    context = {
        'restaurants': restaurants,
        'review_form': review_form,
        'search_form': search_form,  # Tambahkan search_form ke konteks
    }

    return render(request, "review_main.html", context)

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restor, id=id)
    restaurant_reviews = restaurant.reviews.all()
    context = {
        'restaurant': restaurant,
        'restaurant_reviews': restaurant_reviews
    }
    
    return render(request, 'restaurant_detail.html', context)

@csrf_exempt
def add_review(request, id):
    restaurant = get_object_or_404(Restor, id=id)
    
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login required'})
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
            
            # Re-fetch reviews to ensure we have the latest data
            restaurant_reviews = restaurant.reviews.all()
            
            if not restaurant_reviews:
                # Handle empty reviews case
                reviews_html = '''
                <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                    <img src="/static/image/sedih-banget.png" alt="No Reviews" class="w-32 h-32 mb-4"/>
                    <p class="text-center text-gray-600 mt-4">No reviews yet</p>
                </div>
                '''
            else:
                # Render reviews
                reviews_html = ""
                for review in restaurant_reviews:
                    reviews_html += render_to_string('card_review.html', 
                        {'review': review}, 
                        request=request
                    )
            
            return JsonResponse({
                'status': 'success',
                'html': reviews_html
            })
    return JsonResponse({'status': 'error'})

@csrf_exempt
def edit_review(request, id):
    review = get_object_or_404(Review, id=id)
    
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            restaurant = review.restaurant
            restaurant_reviews = restaurant.reviews.all()
            
            reviews_html = ""
            for review in restaurant_reviews:
                reviews_html += render_to_string('card_review.html', {
                    'review': review,
                }, request=request)
            
            return JsonResponse({
                'status': 'success',
                'html': reviews_html
            })
    return JsonResponse({'status': 'error'})

@csrf_exempt
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)
    restaurant = review.restaurant
    review.delete()
    
    restaurant_reviews = restaurant.reviews.all()
    reviews_html = ""
    for review in restaurant_reviews:
        reviews_html += render_to_string('card_review.html', {
            'review': review,
        }, request=request)
    
    return JsonResponse({
        'status': 'success',
        'html': reviews_html if reviews_html else '''
                <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                    <img src="/static/image/sedih-banget.png" alt="No Reviews" class="w-32 h-32 mb-4"/>
                    <p class="text-center text-gray-600 mt-4">No reviews yet</p>
                </div>
                '''
    })

    
