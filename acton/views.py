from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'index.html', {})

@login_required
def inbox(request):
    return render(request, 'inbox.html', {})

def test(request):
    return render(request, 'test.html', {})
