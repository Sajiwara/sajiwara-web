from django.shortcuts import render
from search.models import Restaurant

def show_search(request):
    # Mendapatkan parameter dari URL (GET)
    query_name = request.GET.get('nama')
    query_jenis = request.GET.get('jenis_makanan')
    query_rating = request.GET.get('rating')
    sort_by = request.GET.get('sort_by', 'nama')  # Default sort by nama

    # Cek apakah ada input pencarian (salah satu filter digunakan)
    if query_name or query_jenis or query_rating:
        restaurants = Restaurant.objects.all()

        if query_name:
            restaurants = restaurants.filter(nama__icontains=query_name)
        if query_jenis and query_jenis != "any":
            restaurants = restaurants.filter(jenis_makanan__icontains=query_jenis)
        if query_rating and query_rating != "any":
            # Logika pencarian dalam rentang rating
            if query_rating == "1":
                restaurants = restaurants.filter(rating__gte=1, rating__lt=2)
            elif query_rating == "2":
                restaurants = restaurants.filter(rating__gte=2, rating__lt=3)
            elif query_rating == "3":
                restaurants = restaurants.filter(rating__gte=3, rating__lt=4)
            elif query_rating == "4":
                restaurants = restaurants.filter(rating__gte=4, rating__lte=5)

        # Urutkan hasil pencarian berdasarkan pilihan pengguna
        restaurants = restaurants.order_by(sort_by)

        # Jika tidak ada restoran yang cocok, kirimkan pesan
        if not restaurants.exists():
            message = "nggak ada yg cocok bjir"
        else:
            message = None
    else:
        # Jika belum ada pencarian, tidak menampilkan restoran
        restaurants = None
        message = "mau makan apa?"

    return render(request, 'search.html', {'restaurants': restaurants, 'message': message})
