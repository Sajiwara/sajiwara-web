from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Makanan
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
@login_required(login_url='/login')
def makanan_list(request):
    # Ambil semua data dari model Makanan
    makanan = Makanan.objects.all()

    # Membuat dictionary untuk menyimpan tipe makanan berdasarkan preferensi negara
    makanan_by_preferensi = {}

    # Mengelompokkan makanan berdasarkan preferensi
    for item in makanan:
        if item.preferensi not in makanan_by_preferensi:
            makanan_by_preferensi[item.preferensi] = []
        makanan_by_preferensi[item.preferensi].append(item.menu)

    # Kirim data ke template
    context = {
        'makanan_by_preferensi': makanan_by_preferensi
    }
    return render(request, 'makanan_list.html', {'makanan_by_preferensi': makanan_by_preferensi})