from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import WishlistMenu
from .forms import WishlistForm
from django.shortcuts import render

# View untuk menambahkan wishlist dengan AJAX
def add_to_wishlist(request):
    if request.method == 'POST' and request.is_ajax():
        form = WishlistForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = request.user  # Hubungkan dengan user yang sedang login
            wishlist_item.save()
            return JsonResponse({'status': 'success', 'message': 'Wishlist added successfully!'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'failed'})

# View untuk menampilkan halaman wishlist
def wishlist_page(request):
    wishlist = WishlistMenu.objects.filter(user=request.user)
    return render(request, 'wishlist_page.html', {'wishlist': wishlist})

# View untuk menandai menu sebagai sudah dicoba
def mark_as_tried(request, id):
    if request.method == 'POST' and request.is_ajax():
        wishlist_item = get_object_or_404(WishlistMenu, id=id, user=request.user)
        wishlist_item.tried = True  # Ubah status menjadi "sudah dicoba"
        wishlist_item.save()
        return JsonResponse({'status': 'success', 'message': 'Wishlist item marked as tried!'})
    return JsonResponse({'status': 'failed'})

# View untuk menghapus item dari wishlist
def delete_wishlist_item(request, id):
    if request.method == 'POST' and request.is_ajax():
        wishlist_item = get_object_or_404(WishlistMenu, id=id, user=request.user)
        wishlist_item.delete()  # Hapus item dari wishlist
        return JsonResponse({'status': 'success', 'message': 'Wishlist item deleted!'})
    return JsonResponse({'status': 'failed'})
