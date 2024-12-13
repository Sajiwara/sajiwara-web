from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import PreferensiForm, MakananUpdateForm
from .models import Makanan
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
# Create your views here.

@csrf_exempt

def makanan_list(request):
    form = PreferensiForm(request.POST or None)
    makanan_filtered = Makanan.objects.all()
    
    if request.method == 'POST' and form.is_valid():
        preferensi_terpilih = form.cleaned_data['preferensi']
        if preferensi_terpilih:
            makanan_filtered = Makanan.objects.filter(preferensi=preferensi_terpilih)

    context = {
        'form': form,
        'makanan_filtered': makanan_filtered
    }
    return render(request, 'makanan_list.html', context)

@login_required(login_url='/login')  # Mengarahkan ke halaman login jika belum login
def edit_makanan(request, pk):
    makanan = get_object_or_404(Makanan, pk=pk)
    if request.method == 'POST':
        form = MakananUpdateForm(request.POST, instance=makanan)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = MakananUpdateForm(instance=makanan)
        form_html = render_to_string('edit_makanan.html', {'form': form, 'makanan': makanan}, request=request)
        return JsonResponse({'form_html': form_html})

def show_xml_by_id(request, id):
    data = Makanan.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Makanan.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json(request):
    data = Makanan.objects.filter()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml(request):
    data = Makanan.objects.filter()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
