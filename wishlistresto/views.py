from django.shortcuts import get_object_or_404, render, redirect
from .models import Resto
from .forms import SearchRestoForm

# def show_wishlist(request):
#     restoran = Resto.objects.all()
#     search_form = SearchRestoForm()

#     if request.method == 'POST':
#         search_form = SearchRestoForm(request.POST)
#         if search_form.is_valid():
#             query = search_form.cleaned_data['query'].strip()
#             resto = Resto.objects.GET(restaurant=query)
#             # Tambahkan restoran ke wishlist pengguna
#             # resto.users.add(request.user)
#             return redirect('resto_list')  # Kembali ke daftar restoran
#     return render(request, 'show_wishlistresto.html', {'restoran': restoran, 'form': search_form})

# def show_wishlist(request):
#     restoran = Resto.objects.all()  # Ambil semua restoran
#     search_form = SearchRestoForm()

#     if request.method == 'POST':
#         search_form = SearchRestoForm(request.POST)
#         if search_form.is_valid():
#             query = search_form.cleaned_data['query'].strip()
#             # Menggunakan get() untuk mengambil restoran berdasarkan nama
#             try:
#                 resto = Resto.objects.get(restaurant=query)  # Menggunakan get() yang benar
#                 # Jika restoran ditemukan, kita bisa melakukan sesuatu (misalnya, menambahkannya ke wishlist)
#                 # resto.users.add(request.user)  # Komentar ini jika tidak ingin menambahkannya ke wishlist pengguna yang tidak login
#                 return render(request, 'show_wishlistresto.html', {'restoran': [resto], 'form': search_form})  # Hanya tampilkan restoran yang dicari
#             except Resto.DoesNotExist:
#                 # Jika restoran tidak ditemukan, kita bisa menampilkan pesan atau mengarahkan kembali
#                 return render(request, 'show_wishlistresto.html', {'restoran': [], 'form': search_form, 'error': 'Restoran tidak ditemukan.'})

#     return render(request, 'show_wishlistresto.html', {'restoran': restoran, 'form': search_form})


# def show_wishlist(request):
#     restoran = Resto.objects.all()  # Ambil semua restoran
#     search_form = SearchRestoForm()
#     results = []  # Untuk menyimpan hasil pencarian

#     if request.method == 'POST':
#         search_form = SearchRestoForm(request.POST)
#         if search_form.is_valid():
#             query = search_form.cleaned_data['query'].strip()
#             # Menggunakan filter() untuk mendapatkan semua restoran yang mengandung query
#             results = Resto.objects.filter(restaurant__icontains=query)  # Pencarian tidak sensitif huruf besar/kecil
#             if not results.exists():
#                 error_message = 'Tidak ada restoran yang ditemukan sesuai pencarian.'
#                 return render(request, 'show_wishlistresto.html', {
#                     'restoran': results, 
#                     'form': search_form,
#                     'error_message': error_message  # Kirim pesan kesalahan ke template
#                 })

#     return render(request, 'show_wishlistresto.html', {
#         'restoran': results, 
#         'form': search_form,
#     })

def show_wishlist(request):
    # Ambil semua restoran
    restoran = Resto.objects.all()
    wishlist_restaurants = Resto.objects.filter(visited=False)  # Restoran yang belum dikunjungi
    visited_restaurants = Resto.objects.filter(visited=True)  # Restoran yang sudah dikunjungi

    search_form = SearchRestoForm()
    results = []  # Untuk menyimpan hasil pencarian
    error_message = None  # Pesan kesalahan, jika ada

    if request.method == 'POST':
        search_form = SearchRestoForm(request.POST)
        if search_form.is_valid():
            query = search_form.cleaned_data['query'].strip()
            # Menggunakan filter() untuk mendapatkan semua restoran yang mengandung query
            results = Resto.objects.filter(restaurant__icontains=query)  # Pencarian tidak sensitif huruf besar/kecil
            
            # Cek jika tidak ada hasil
            if not results.exists():
                error_message = 'Tidak ada restoran yang ditemukan sesuai pencarian.'
    
    # Menangani penambahan ke wishlist
    if request.GET.get('add_to_wishlist'):
        resto_id = request.GET.get('add_to_wishlist')
        resto = get_object_or_404(Resto, id=resto_id)

        # Cek apakah restoran sudah ada di wishlist
        if resto.visited:
            error_message = 'Restoran sudah ada dalam wishlist.'
        else:
            resto.visited = False  # Pastikan statusnya tidak dikunjungi
            resto.save()
            return redirect('show_wishlist')  # Kembali ke daftar wishlist

    # Menangani update status menjadi telah dikunjungi
    if request.GET.get('mark_visited'):
        resto_id = request.GET.get('mark_visited')
        resto = get_object_or_404(Resto, id=resto_id)
        resto.visited = True  # Update status menjadi telah dikunjungi
        resto.save()
        return redirect('show_wishlist')  # Kembali ke daftar wishlist

    return render(request, 'show_wishlistresto.html', {
        'wishlist_restaurants': wishlist_restaurants,  # Restoran yang belum dikunjungi
        'visited_restaurants': visited_restaurants,  # Restoran yang sudah dikunjungi
        'form': search_form,
        'error_message': error_message  # Kirim pesan kesalahan ke template
    })