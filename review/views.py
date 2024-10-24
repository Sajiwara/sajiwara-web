from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Restor
from .models import Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import ReviewForm
# Create your views here.

def show_main(request):
    restaurants = Restor.objects.all()

    context = {
        'restaurants' : restaurants
    }

    return render(request, "review_main.html", context)

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restor, pk=id)
    restaurant_reviews = restaurant.reviews.all()
    context = {
        'restaurant': restaurant,
        'restaurant_reviews': restaurant_reviews
    }
    
    return render(request, 'restaurant_detail.html', context)

def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restor, id=restaurant_id)  # Make sure the restaurant is correctly fetched
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)  # Don't save the review yet
        review.user = request.user  # Assign the user who submitted the review
        review.restaurant = restaurant  # Link the review to the current restaurant
        review.save()  # Now save the review with the assigned fields
        return redirect('review:restaurant_detail', id=restaurant_id)

    context = {'form': form, 'restaurant': restaurant}
    return render(request, "add_review.html", context)

def delete_review(request, review_id):
    review = Review.objects.get(pk =review_id)
    review.delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('review:show_main')))  # Redirect back



    
