from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Resto
from .forms import SearchRestoForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required(login_url='/login')
# def show_wishlistresto(request):
#     wishlist_restaurants = Resto.objects.filter(user=request.user, wanted_resto=True)  # Filter by user
#     visited_restaurants = Resto.objects.filter(user=request.user, visited=True)  # Filter by user

#     context = {
#         'wishlist_restaurants': wishlist_restaurants,
#         'visited_restaurants': visited_restaurants,
#     }
#     return render(request, 'show_wishlistresto.html', context)

def show_wishlistresto(request):
    wishlist_restaurants = Resto.objects.filter( wanted_resto=True)
    visited_restaurants = Resto.objects.filter(visited=True)

    context = {
        'wishlist_restaurants': wishlist_restaurants,
        'visited_restaurants': visited_restaurants,
    }
    return render(request, 'show_wishlistresto.html', context)

# def add_to_wishlist(request):
#     form = SearchRestoForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         resto = form.save(commit=False)
#         form.save()
#         return redirect('wishlistresto:show_wishlistresto')
    
#     context = {'form': form}
#     return render(request, "add_to_wishlist.html", context)

@csrf_exempt
def add_to_wishlist(request):
    form = SearchRestoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Mengambil nama restoran dari form
        resto_name = form.cleaned_data.get('restaurant')

        resto = Resto.objects.get(restaurant=resto_name)
        # resto.user = request.user

        # Jika restoran sudah ada, update wanted_resto menjadi True
        resto.wanted_resto = True
        resto.save()  # Simpan perubahan

        return redirect('wishlistresto:show_wishlistresto')

    context = {'form': form}
    return render(request, "add_to_wishlist.html", context)

# def add_to_wishlist(request):
#     form = SearchRestoForm(request.POST or None)

#     if request.method == "POST" and form.is_valid():
#         # Get restaurant name from the form
#         resto_name = form.cleaned_data.get('restaurant')

#         # Check if the restaurant already exists for the user
#         resto, created = Resto.objects.get_or_create(
#             restaurant=resto_name,
#             user=request.user,  # Set the current user
#             defaults={'wanted_resto': True}
#         )

#         # If the restaurant already existed, just update wanted_resto
#         if not created:
#             resto.wanted_resto = True
#             resto.save()  # Save changes

#         return redirect('wishlistresto:show_wishlistresto')

#     context = {'form': form}
#     return render(request, "add_to_wishlist.html", context)

@csrf_exempt
def visited_resto(request, id):
    resto = Resto.objects.get(pk=id)
    resto.visited = True
    resto.save()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

@csrf_exempt
def not_visited_resto(request, id):
    resto = Resto.objects.get(pk=id)
    resto.visited = False
    resto.save()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

@csrf_exempt
def delete_wishlist(request, id):
    resto = Resto.objects.get(pk=id)
    resto.wanted_resto = False
    resto.save()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

# @csrf_exempt
# def visited_resto(request, id):
#     resto = get_object_or_404(Resto, pk=id, user=request.user)  # Get restaurant for the user
#     resto.visited = True
#     resto.save()
#     return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

# @csrf_exempt
# def not_visited_resto(request, id):
#     resto = get_object_or_404(Resto, pk=id, user=request.user)  # Get restaurant for the user
#     resto.visited = False
#     resto.save()
#     return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

# @csrf_exempt
# def delete_wishlist(request, id):
#     resto = get_object_or_404(Resto, pk=id, user=request.user)  # Get restaurant for the user
#     resto.wanted_resto = False
#     resto.save()
#     return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))
