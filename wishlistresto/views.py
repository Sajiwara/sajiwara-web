from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from wishlistresto.models import WishlistResto
from .forms import SearchRestoForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from katalog.models import Restonya
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required(login_url='/login')
def show_wishlistresto(request):
    # Mengambil semua restoran dari model Resto
    restos = Restonya.objects.all()
    
    # Mengambil wishlist yang ada (sesuai dengan user, jika ada filter)
    wishlist_restaurants = WishlistResto.objects.filter(user=request.user)
    visited_restaurants = WishlistResto.objects.filter(user=request.user, visited=True)
    
    context = {
        'restos': restos,  # pastikan ini dikirim ke template
        'wishlist_restaurants': wishlist_restaurants,
        'visited_restaurants': visited_restaurants
    }
    return render(request, 'show_wishlistresto.html', context)


@csrf_exempt
def add_to_wishlist(request):
    if request.method == "POST":
        form = SearchRestoForm(request.POST)
        if form.is_valid():
            # Get restaurant instance from the form
            resto_instance = form.cleaned_data.get('restaurant')

            # Check if the restaurant already exists for the user
            resto, created = WishlistResto.objects.get_or_create(
                restaurant_wanted=resto_instance.restaurant,
                user=request.user,  # Set the current user
                defaults={'wanted_resto': True}
            )

            # If the restaurant already existed, just update wanted_resto
            if not created:
                resto.wanted_resto = True
                resto.save()  # Save changes

            # AJAX response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Restoran berhasil ditambahkan ke wishlist!',
                    'restaurant': resto.restaurant_wanted
                })

        # Jika form tidak valid
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Gagal menambahkan restoran. Periksa form Anda.'
            })

    # Load restoran dari model Resto
    restos = Restonya.objects.all()

    # Kirimkan form dan data resto ke template
    context = {'form': SearchRestoForm(), 'restos': restos}
    return render(request, "show_wishlistresto.html", context)

@csrf_exempt
def add_to_wishlist_flutter(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'status': 'error', 'message': 'User must be logged in'}, status=401)

            data = json.loads(request.body)
            print("Data yang diterima: ", data)  # Debugging untuk melihat payload dari Flutter

            new_wishlist = WishlistResto.objects.create(
                user=request.user,
                restaurant_wanted=data.get('restaurant_wanted'),
                wanted_resto=data.get('wanted_resto'),
                visited=data.get('visited'),
            )

            new_wishlist.save()

            return JsonResponse({'status': 'success', 'message': 'Data berhasil diterima'}, status=201)
        except Exception as e:
            print("Error saat memproses data: ", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def visited_resto_flutter(request, id):
    if request.method == "POST":
        # Pastikan user sudah login
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User is not authenticated"
            }, status=401)

        # Ambil objek WishlistResto yang sesuai
        try:
            resto = get_object_or_404(WishlistResto, pk=id, user=request.user)
        except WishlistResto.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Restaurant not found"
            }, status=404)

        # Tandai restoran sebagai "visited"
        resto.visited = True
        resto.save()

        return JsonResponse({
            "status": True,
            "message": f"Restaurant '{resto.restaurant_wanted}' marked as visited!"
        })

    # Jika bukan POST request, kirimkan error
    return JsonResponse({
        "status": False,
        "message": "Invalid request method"
    }, status=400)

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
def delete_wishlist_flutter(request, id):
    if request.method == "POST":  # Gunakan POST untuk menggantikan DELETE
        resto = get_object_or_404(WishlistResto, pk=id, user=request.user)
        resto.delete()
        return JsonResponse({"status": True, "message": "Wishlist deleted successfully."})
    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def delete_wishlist(request, id):
    resto = get_object_or_404(WishlistResto, pk=id, user=request.user)  # Get restaurant for the user
    resto.delete()
    return HttpResponseRedirect(reverse('wishlistresto:show_wishlistresto'))

def show_json(request):
    data = WishlistResto.objects.filter(user=request.user, wanted_resto=True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    # wishlist = WishlistResto.objects.all().values()
    # return JsonResponse(list(data), safe=False)

def get_json_resto_data(request):
    qs_val= list(Restonya.objects.values())
    return JsonResponse({'data':qs_val})
