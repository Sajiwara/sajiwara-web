from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import WishlistMenu, Menu, Restaurant  # Ensure you import the correct models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils.decorators import method_decorator
import json


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
    menu_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)  
    menu_item.tried = False
    menu_item.save()
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

# View untuk menghapus item dari wishlist
@csrf_exempt
def delete_wishlist(request, id):
    menu_item = get_object_or_404(WishlistMenu, pk=id, user=request.user) 
    menu_item.delete()
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

def show_json(request):
    data = WishlistMenu.objects.filter(user=request.user, wanted_menu=True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_json_menu_data(request):
    qs_val = list(Menu.objects.values())
    return JsonResponse({'data': qs_val})


@csrf_exempt
def show_wishlistmenu_api(request):
    menus = Menu.objects.filter(wishlistmenu__user=request.user).distinct()
    menus_data = [{'id': menu.id, 'menu': menu.menu, 'restaurant': menu.restaurant.name} for menu in menus]

    wishlist_menus = WishlistMenu.objects.filter(user=request.user)
    wishlist_data = [
        {
            'id': item.id,
            'menu_name': item.menu_wanted.menu,
            'restaurant_name': item.menu_wanted.restaurant.name,
            'tried': item.tried
        } for item in wishlist_menus
    ]

    tried_menus = WishlistMenu.objects.filter(user=request.user, tried=True)
    tried_data = [
        {
            'id': item.id,
            'menu_name': item.menu_wanted.menu,
            'restaurant_name': item.menu_wanted.restaurant.name
        } for item in tried_menus
    ]

    return JsonResponse({
        'menus': menus_data,
        'wishlist_menus': wishlist_data,
        'tried_menus': tried_data
    }, safe=False)

@csrf_exempt
def show_menus_api(request):
    menus = Menu.objects.values_list('menu', flat=True).distinct()
    menu_list = list(menus)
    return JsonResponse({'menus': menu_list})

@csrf_exempt
def show_restaurants_api(request):
    menu = request.GET.get('menu', None)
    restaurants = Restaurant.objects.filter(menus__menu__icontains=menu).distinct()
    restaurant_list = list(restaurants.values())
    return JsonResponse({'restaurants': restaurant_list})

@csrf_exempt
@login_required(login_url='/login')
def add_wishlistmenu_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            menu_name = data.get('menu')
            restaurant_id = data.get('restaurant')

            if menu_name and restaurant_id:
                menu_instance = get_object_or_404(Menu, menu=menu_name, restaurant=restaurant_id)

                wishlist_item, created = WishlistMenu.objects.get_or_create(
                    menu_wanted=menu_instance,
                    user=request.user,
                    defaults={'wanted_menu': True}
                )

                if not created:
                    wishlist_item.wanted_menu = True
                    wishlist_item.save()

                return JsonResponse({'success': True, 'message': 'Menu added to wishlist successfully!'})

            return JsonResponse({'success': False, 'message': 'Invalid data provided.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def update_tried_status_api(request, id):
    try:
        data = json.loads(request.body)
        tried_status = data.get('tried', None)

        menu_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)
        if tried_status is not None:
            menu_item.tried = tried_status
            menu_item.save()

            return JsonResponse({'success': True, 'message': f"Menu marked as {'tried' if tried_status else 'not tried'} successfully!"})

        return JsonResponse({'success': False, 'message': 'Invalid tried status.'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)

@csrf_exempt
def show_triedmenu_api(request):
    tried_menus = WishlistMenu.objects.filter(user=request.user, tried=True)
    tried_data = [
        {
            'id': item.id,
            'menu_name': item.menu_wanted.menu,
            'restaurant_name': item.menu_wanted.restaurant.name,    
            'tried': item.tried
        } for item in tried_menus
    ]

    return JsonResponse({'tried_menus': tried_data}, safe=False)

@csrf_exempt
@login_required(login_url='/login')
def delete_wishlist_api(request, id):
    menu_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)
    menu_item.delete()
    return JsonResponse({'success': True, 'message': 'Menu deleted from wishlist successfully!'})

@login_required(login_url='/login')
def show_json_api(request):
    data = WishlistMenu.objects.filter(user=request.user, wanted_menu=True)
    serialized_data = serializers.serialize("json", data)
    return JsonResponse({'data': json.loads(serialized_data)})

@csrf_exempt
def get_json_menu_data_api(request):
    menus = list(Menu.objects.values())
    return JsonResponse({'menus': menus})