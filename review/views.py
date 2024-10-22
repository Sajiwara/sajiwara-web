from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Restor
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def show_main(request):
    restaurants = Restor.objects.all()

    context = {
        'restaurants' : restaurants
    }

    return render(request, "review_main.html", context)

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restor, pk=id)
    context = {'restaurant': restaurant}
    return render(request, 'restaurant_detail.html', context)