from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if 'next' in request.POST:
                response = HttpResponseRedirect(request.POST['next'])
            else:
                response = HttpResponseRedirect(reverse("landingpage:show_landingpage")) 
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)
    
@csrf_exempt
def logout(request):
    auth_logout(request)
    response = HttpResponseRedirect(reverse('landingpage:show_landingpage'))
    return response

def show_landingpage(request):
    context = {
        'kelompok' : 'c 12',
        'class': 'PBP c'
    }

    return render(request, "landingpage.html", context)

def register(request):
    form = UserCreationForm() 

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('landingpage:login')
    context = {'form':form}
    return render(request, 'register.html', context)

# def search(request):
#     return render(request, 'search.html')

# def explore(request):
#     return render(request, 'explore.html')

# def add_review(request):
#     return render(request, 'review.html')