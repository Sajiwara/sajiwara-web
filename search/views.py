from django.shortcuts import render
from search.models import Restaurant
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required



def show_search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Mendapatkan parameter dari URL (GET)
        query_name = request.GET.get('nama')
        query_jenis = request.GET.get('jenis_makanan')
        query_rating = request.GET.get('rating')
        sort_by = request.GET.get('sort_by', 'nama')
       
        restaurants = Restaurant.objects.all()

        if query_name:
            restaurants = restaurants.filter(nama__icontains=query_name)
        if query_jenis and query_jenis != "any":
            restaurants = restaurants.filter(jenis_makanan__icontains=query_jenis)
        if query_rating and query_rating != "any":
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

        if sort_by in ['nama', '-nama', 'rating', '-rating', 'harga', '-harga', 'jarak', '-jarak']:
            restaurants = restaurants.order_by(sort_by)

        message = "Tidak ada data yang cocok" if not restaurants.exists() else None

        # Tambahkan nama di message
        search_title = f'Hasil Pencarian untuk "{query_name}"' if query_name else "Hasil Pencarian"


        context = {
            'restaurants': restaurants,
            'message': message,
            'search_title': search_title,
            'is_authenticated': request.user.is_authenticated  # Status login pengguna
        }

        result_html = render_to_string('search_results.html', context)
        return JsonResponse({
            'html': result_html
        })

    return render(request, 'search.html')



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

