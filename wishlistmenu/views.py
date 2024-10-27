from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import WishlistMenu, Menu  # Ensure you import the correct models
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
def add_to_wishlistmenu(request):
    if request.method == "POST":
        menu_id = request.POST.get('menu')  # Ambil ID menu dari form
        if menu_id:
            menu_instance = get_object_or_404(Menu, id=menu_id)  # Ambil instance Menu berdasarkan ID

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
    data = WishlistMenu.objects.filter(user=request.user, wanted_menu=True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_json_menu_data(request):
    qs_val = list(Menu.objects.values())
    return JsonResponse({'data': qs_val})