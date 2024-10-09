from django.shortcuts import render

# Create your views here.
def show_landingpage(request):
    context = {
        'kelompok' : 'c 12',
        'class': 'PBP c'
    }

    return render(request, "landingpage.html", context)