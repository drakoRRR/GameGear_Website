from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'users/login_page.html')

def register(request):
    return render(request, 'users/register_page.html')