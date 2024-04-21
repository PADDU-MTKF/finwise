from django.shortcuts import render,HttpResponse, redirect

# Create your views here.
def temp(request):
    if request.method=="POST":
        if 'team' in request.POST:
            return redirect('team_view')
        if 'finance' in request.POST:
            return redirect('finance_view')
        if 'work' in request.POST:
            return redirect('work_view')
    return render(request, 'adminHome.html')


def home(request):
    return render(request, 'login.html')

def team_view(request):
    # Your logic for team management view
    return render(request, 'adminteam.html')


def finance_view(request):
    # Your logic for finance management view
    return render(request, 'adminfinance.html')


def work_view(request):
    # Your logic for work staging view
    return render(request, 'adminwork.html')
