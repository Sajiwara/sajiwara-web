import json
import uuid
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

def show_json_restoran(request):
    data = Restor.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_review(request, id):
    # Mengambil restoran berdasarkan UUID
    restaurant = get_object_or_404(Restor, id=id)

    # Mengambil semua review untuk restoran tersebut
    reviews = Review.objects.filter(restaurant=restaurant)

    # Custom serialization
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            "id": str(review.id),
            "user": {
                "id": review.user.id,
                "username": review.user.username,
            },
            "restaurant": str(review.restaurant.id),
            "review": review.review,
            "date_posted": review.date_posted.isoformat(),
        })

    # Mengembalikan data dalam format JSON
    return JsonResponse(reviews_data, safe=False)

# @csrf_exempt
# def create_review_flutter(request):
#     if request.method == 'POST':

#         data = json.loads(request.body)
#         print("data yang diterima ", data)
#         new_review = Review.objects.create(
#             user=request.user,
#             review=data["review"],
           
#         )

#         new_review.save()

#         return JsonResponse({"status": "success"}, status=200)
#     else:
#         return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def create_review_flutter(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login required'})

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            restaurant_id = data.get('restaurant')
            review_text = data.get('review')

            if not restaurant_id or not review_text:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'})

            restaurant = Restor.objects.get(id=restaurant_id)
            review = Review.objects.create(
                user=request.user,
                restaurant=restaurant,
                review=review_text
            )
            return JsonResponse({
                'status': 'success',
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def get_user_info(request):
    user = request.user
    return JsonResponse({
        "id": user.id,  # ID pengguna
        "username": user.username,  # Username pengguna
    })

@csrf_exempt
def edit_review_flutter(request, id):
    try:
        # Pastikan id adalah UUID
        uuid_id = uuid.UUID(str(id))
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid UUID'}, status=400)

    # Ambil review berdasarkan UUID
    review = get_object_or_404(Review, id=uuid_id)

    if request.method == "POST":
        data = json.loads(request.body)  # Pastikan JSON body diterima
        review_text = data.get('review_text')
    if not review_text:
        return JsonResponse({'status': 'error', 'message': 'Review text is missing'}, status=400)
    
    form = ReviewForm({'review': review_text}, instance=review)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Review updated successfully'})
    else:
        print(form.errors)  # Debug error form
        return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)

@csrf_exempt
def flutter_delete_review(request, id):
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        try:
            review = get_object_or_404(Review, id=id)
            review.delete()
            return JsonResponse({'success': True, 'status': 'success', 'message': 'Review deleted successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

