from django.shortcuts import render
from search.models import Restaurant
from django.http import HttpResponse
from django.core import serializers

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
            elif query_rating == "0":
                restaurants = restaurants.filter(rating__gte=0, rating__lte=1)


        # Urutkan hasil pencarian berdasarkan pilihan pengguna
        if sort_by in ['nama', '-nama', 'rating', '-rating', 'harga', '-harga', 'jarak', '-jarak']:
            restaurants = restaurants.order_by(sort_by)

        # Jika tidak ada restoran yang cocok, kirimkan pesan
        if not restaurants.exists():
            message = "Tidak ada data yang cocok"
        else:
            message = None
    else:
        # Jika belum ada pencarian, tidak menampilkan restoran
        restaurants = None
        message = "Mau makan apa hari ini?"

    return render(request, 'search.html', {'restaurants': restaurants, 'message': message})


def show_xml(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Restaurant.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Restaurant.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")