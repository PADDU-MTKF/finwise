from django.shortcuts import render,HttpResponse

# Create your views here.
def temp(request):
    return render(request, 'adminHome.html')

def home(request):
    return render(request, 'login.html')
