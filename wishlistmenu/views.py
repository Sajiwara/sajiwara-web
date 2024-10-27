from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Menu, WishlistMenu
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers
from django.http import HttpResponseRedirect


@csrf_exempt
@login_required(login_url='/login')
def show_wishlistmenu(request):
    # Fetch all menu items
    menus = Menu.objects.all()
    
    # Fetch the user's wishlist
    wishlist_items = WishlistMenu.objects.filter(user=request.user)
    tried_items = WishlistMenu.objects.filter(user=request.user, tried=True)
    
    context = {
        'menus': menus,  # Include all menu items for dropdown
        'wishlist_items': wishlist_items,
        'tried_items': tried_items,
    }
    return render(request, 'show_wishlistmenu.html', context)

@csrf_exempt
def add_to_wishlist(request):
    if request.method == "POST":
        menu_id = request.POST.get('menu')  # Get selected menu ID from the form
        if menu_id:
            menu_instance = get_object_or_404(Menu, id=menu_id)  # Get the menu instance

            # Check if the menu item already exists in the user's wishlist
            wishlist_item, created = WishlistMenu.objects.get_or_create(
                menu_wanted=menu_instance.menu,
                user=request.user,  # Set the current user
                defaults={'wanted_menu': True}
            )

            if not created:
                # If already in the wishlist, just update the wanted_menu
                wishlist_item.wanted_menu = True
                wishlist_item.save()  # Save changes

            # AJAX response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Menu berhasil ditambahkan ke wishlist!',
                    'menu': wishlist_item.menu_wanted
                })

        # If menu_id is not provided
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Gagal menambahkan menu. Periksa form Anda.'
            })

    # In case of a GET request, redirect to the wishlist menu page
    return redirect('wishlistmenu:show_wishlistmenu')

@csrf_exempt
def tried_menu(request, id):
    # Mark a wishlist menu item as tried
    wishlist_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)
    wishlist_item.tried = True
    wishlist_item.save()
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

@csrf_exempt
def not_tried_menu(request, id):
    # Mark a wishlist menu item as not tried
    wishlist_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)
    wishlist_item.tried = False
    wishlist_item.save()
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

@csrf_exempt
def delete_wishlist(request, id):
    # Delete a wishlist menu item
    wishlist_item = get_object_or_404(WishlistMenu, pk=id, user=request.user)
    wishlist_item.delete()
    return HttpResponseRedirect(reverse('wishlistmenu:show_wishlistmenu'))

def show_json(request):
    # Show all wishlist items for the user in JSON format
    data = WishlistMenu.objects.filter(user=request.user, wanted_menu=True)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
