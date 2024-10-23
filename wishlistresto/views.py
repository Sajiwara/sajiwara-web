from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Resto, WishlistResto
from .forms import SearchRestoForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers

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

# @csrf_exempt
# @login_required(login_url='/login')
# def show_wishlistresto(request):
   
#     context = {
#    }
#     return render(request, 'show_wishlistresto.html', context)



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

# @csrf_exempt
# def add_to_wishlist(request):
#     resto_name = request.POST.get('restaurant')
#     user = request.user
    
#     if resto_name:
#         wanted = WishlistResto(restaurant_wanted=resto_name, user=user, wanted_resto=True)
#         wanted.save()
#         return HttpResponse(b"CREATED", status=201)
#     else:
#         return HttpResponse(b"BAD REQUEST", status=400)

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
    resto.delete()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

def show_json(request):
    data = WishlistResto.objects.filter(user=request.user, wanted_resto=True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.shortcuts import get_object_or_404, render, redirect
# from django.urls import reverse
# from .models import Resto, WishlistResto
# from .forms import SearchRestoForm
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from django.core import serializers
# from django.template.loader import render_to_string

# @csrf_exempt
# @login_required(login_url='/login')
# def show_wishlistresto(request):
#     wishlist_restaurants = WishlistResto.objects.filter(user=request.user, wanted_resto=True)
#     visited_restaurants = WishlistResto.objects.filter(user=request.user, visited=True)

#     context = {
#         'wishlist_restaurants': wishlist_restaurants,
#         'visited_restaurants': visited_restaurants,
#     }
#     return render(request, 'show_wishlistresto.html', context)

# # @csrf_exempt
# # @login_required(login_url='/login')
# # def add_to_wishlist(request):
# #     if request.method == "GET" and request.is_ajax():
# #         form = SearchRestoForm()
# #         return render(request, 'wishlistresto/wishlist_form.html', {'form': form})
    
# #     return JsonResponse({'error': 'Invalid request'}, status=400)

# @csrf_exempt
# @login_required(login_url='/login')
# def add_to_wishlist(request):
#     form = SearchRestoForm(request.POST or None)

#     if request.method == "POST":
#         if form.is_valid():
#             resto_name = form.cleaned_data.get('restaurant')
#             resto, created = WishlistResto.objects.get_or_create(
#                 restaurant_wanted=resto_name,
#                 user=request.user,
#                 defaults={'wanted_resto': True}
#             )

#             if not created:
#                 resto.wanted_resto = True
#                 resto.save()

#             return JsonResponse({'success': True})

#         else:
#             return JsonResponse({'success': False, 'form_html': render_to_string('wishlistresto/wishlist_form.html', {'form': form})})

#     return JsonResponse({'error': 'Invalid request'}, status=400)

# @csrf_exempt
# @login_required(login_url='/login')
# def visited_resto(request, id):
#     resto = get_object_or_404(WishlistResto, pk=id, user=request.user)
#     resto.visited = True
#     resto.save()
#     return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

# @csrf_exempt
# @login_required(login_url='/login')
# def not_visited_resto(request, id):
#     resto = get_object_or_404(WishlistResto, pk=id, user=request.user)
#     resto.visited = False
#     resto.save()
#     return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

# @csrf_exempt
# @login_required(login_url='/login')
# def delete_wishlist(request, id):
#     resto = get_object_or_404(WishlistResto, pk=id, user=request.user)
#     resto.delete()
#     return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

# def show_json(request):
#     data = WishlistResto.objects.filter(user=request.user, wanted_resto=True)
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")

