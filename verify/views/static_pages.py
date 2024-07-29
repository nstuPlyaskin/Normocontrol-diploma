from django.shortcuts import render


def index(request):
    """Главная страница информационной системы."""
    return render(request, 'verify/index.html')
