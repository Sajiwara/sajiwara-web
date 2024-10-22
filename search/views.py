from django.shortcuts import render

from search.models import Restaurant

def show_search(request):
    
    return render(request, 'search.html')
