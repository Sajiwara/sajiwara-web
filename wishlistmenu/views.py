import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import WishlistMenu, Menu, Restaurant  # Ensure you import the correct models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

@csrf_exempt
@login_required(login_url='/login')
def show_wishlistmenu(request):
    # Fetch all menu items from the Menu model
    menus = Menu.objects.all()
    
    # Fetch the user's wishlist menu items
    wishlist_menus = WishlistMenu.objects.filter(user=request.user)
    tried_menus = WishlistMenu.objects.filter(user=request.user, tried=True)

    context = {
        'menus': menus,  # Ensure this is sent to the template
        'wishlist_menus': wishlist_menus,
        'tried_menus': tried_menus
    }
    return render(request, 'show_wishlistmenu.html', context)

@csrf_exempt
def show_menus(request):
    menus = Menu.objects.values_list('menu', flat=True).distinct()
    menu_list = list(menus)
    return JsonResponse(menu_list, safe=False)

@csrf_exempt
def show_restaurants(request):
    menu = request.GET.get('menu', None)
    restaurants = Restaurant.objects.filter(
        menus__menu__icontains=menu
    ).distinct()
    restaurant_list = list(restaurants.values())
    return JsonResponse(restaurant_list, safe=False)

@csrf_exempt
def add_to_wishlistmenu(request):
    if request.method == "POST":
        menu_name = request.POST.get('menu')  # Ambil nama menu dari form
        restaurant_id = request.POST.get('restaurant')
        if menu_name and restaurant_id:
            menu_instance = get_object_or_404(Menu, menu=menu_name, restaurant = restaurant_id)  # Ambil instance Menu berdasarkan ID

            # Tambahkan menu ke wishlist untuk user yang sedang login
            wishlist_item, created = WishlistMenu.objects.get_or_create(
                menu_wanted=menu_instance,  # Hubungkan dengan instance Menu
                user=request.user,
                defaults={'wanted_menu': True}
            )

            # Update jika item sudah ada di wishlist
            if not created:
                wishlist_item.wanted_menu = True
                wishlist_item.save()

            # Mengembalikan respons JSON jika permintaan adalah AJAX
            return JsonResponse({
                'success': True,
                'message': 'Menu berhasil ditambahkan ke wishlist!'
            })

        # Jika menu_id tidak valid, kembalikan respons JSON kesalahan
        return JsonResponse({
            'success': False,
            'message': 'Gagal menambahkan menu. Periksa form Anda.'
        }, status=400)

    # Kembalikan halaman biasa jika bukan permintaan POST
    menus = Menu.objects.all()
    context = {'menus': menus}
    return render(request, "show_wishlistmenu.html", context)

@csrf_exempt
@login_required(login_url='/login')
def tried_menu(request, id):
    # Get the wishlist menu item for the user
    menu_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)
    menu_item.tried = True  # Mark the menu as tried
    menu_item.save()  # Save the changes
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

# View untuk menandai item sebagai belum dicoba
@csrf_exempt
def not_tried_menu(request, id):
    menu_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)  # Get menu item for the user
    menu_item.tried = False
    menu_item.save()
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

# View untuk menghapus item dari wishlist
@csrf_exempt
def delete_wishlist(request, id):
    menu_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)  # Get menu item for the user
    menu_item.delete()
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

def show_json(request):
    # Fetch wishlist items for the logged-in user
    data = WishlistMenu.objects.filter(user=request.user, wanted_menu=True)
    
    # Modify the data to include the menu name and restaurant details
    wishlist_data = []
    for item in data:
        # Add the menu name and restaurant details to the response
        menu_name = item.menu_wanted.menu if item.menu_wanted else None
        restaurant_name = item.menu_wanted.restaurant.name if item.menu_wanted and item.menu_wanted.restaurant else None
        wishlist_data.append({
            "model": "wishlistmenu.wishlistmenu",
            "pk": str(item.pk),
            "fields": {
                "menu_wanted": menu_name,  # Instead of ID, return the menu name
                "restaurant": restaurant_name,  # Include restaurant name
                "user": item.user.id,
                "wanted_menu": item.wanted_menu,
                "tried": item.tried
            }
        })
    
    return HttpResponse(json.dumps(wishlist_data), content_type="application/json")

def get_json_menu_data(request):
    qs_val = list(Menu.objects.values())
    return JsonResponse({'data': qs_val})

@csrf_exempt
def add_to_wishlist_flutter(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'status': 'error', 'message': 'User must be logged in'}, status=401)

            data = json.loads(request.body)
            print("Data yang diterima: ", data)  # Debugging untuk melihat payload dari Flutter

            new_wishlist = WishlistMenu.objects.create(
                user=request.user,
                menu_wanted=data.get('menu_wanted'),
                wanted_menu=data.get('wanted_menu'),
                tried=data.get('tried'),
            )

            new_wishlist.save()

            return JsonResponse({'status': 'success', 'message': 'Data berhasil diterima'}, status=201)
        except Exception as e:
            print("Error saat memproses data: ", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def tried_menu_flutter(request, id):
    if request.method == "POST":
        # Pastikan user sudah login
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User is not authenticated"
            }, status=401)

        # Ambil objek WishlistMenu yang sesuai
        try:
            menu = get_object_or_404(WishlistMenu, pk=id, user=request.user)
        except WishlistMenu.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Menu not found"
            }, status=404)

        # Tandai restoran sebagai "tried"
        menu.tried = True
        menu.save()

        return JsonResponse({
            "status": True,
            "message": f"Menu '{menu.menu_wanted}' marked as tried!"
        })

    # Jika bukan POST request, kirimkan error
    return JsonResponse({
        "status": False,
        "message": "Invalid request method"
    }, status=400)

@csrf_exempt
def delete_wishlist_flutter(request, id):
    if request.method == "POST":  # Gunakan POST untuk menggantikan DELETE
        menu = get_object_or_404(WishlistMenu, pk=id, user=request.user)
        menu.delete()
        return JsonResponse({"status": True, "message": "Wishlist deleted successfully."})
    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)
