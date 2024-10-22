from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Resto, WishlistResto
from .forms import SearchRestoForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required(login_url='/login')
def show_wishlistresto(request):
    wishlist_restaurants = WishlistResto.objects.filter(user=request.user, wanted_resto=True)  # Filter by user
    visited_restaurants = WishlistResto.objects.filter(user=request.user, visited=True)  # Filter by user

    context = {
        'wishlist_restaurants': wishlist_restaurants,
        'visited_restaurants': visited_restaurants,
    }
    return render(request, 'show_wishlistresto.html', context)

@csrf_exempt
def add_to_wishlist(request):
    form = SearchRestoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Get restaurant name from the form
        resto_name = form.cleaned_data.get('restaurant')

        # Check if the restaurant already exists for the user
        resto, created = WishlistResto.objects.get_or_create(
            restaurant_wanted=resto_name,
            user=request.user,  # Set the current user
            defaults={'wanted_resto': True}
        )

        # If the restaurant already existed, just update wanted_resto
        if not created:
            resto.wanted_resto = True
            resto.save()  # Save changes

        return redirect('wishlistresto:show_wishlistresto')

    context = {'form': form}
    return render(request, "add_to_wishlist.html", context)

@csrf_exempt
def visited_resto(request, id):
    resto = get_object_or_404(WishlistResto, pk=id, user=request.user)  # Get restaurant for the user
    resto.visited = True
    resto.save()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

@csrf_exempt
def not_visited_resto(request, id):
    resto = get_object_or_404(WishlistResto, pk=id, user=request.user)  # Get restaurant for the user
    resto.visited = False
    resto.save()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

@csrf_exempt
def delete_wishlist(request, id):
    resto = get_object_or_404(WishlistResto, pk=id, user=request.user)  # Get restaurant for the user
    resto.wanted_resto = False
    resto.save()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))
