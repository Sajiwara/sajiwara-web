from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username is not None and password is not None:
        user = authenticate(username=username, password=password)

        if user is not None and user.is_authenticated:
            auth_login(request, user)
            # status sukses
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
            }, status=200)
        else:
            return JsonResponse({
                 "status": False,
                "message": "Login failed, wrong username or password."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Username or password not provided in the request."
        }, status=400)
    
@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)