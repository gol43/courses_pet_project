from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,
                                 'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


def index_view(request):
    return render(request, 'index.html')


def buying_view(request):
    return render(request, 'buying.html')


def courses_view(request):
    return render(request, 'courses.html')
