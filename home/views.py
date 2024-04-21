from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages


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



USERNAME="hello"
PASSWORD="hi"
def logout(request):
    data={'logOut':True}
    return render(request,'login.html',data)


def login(request):
    if request.method == 'POST':
        data={}
        if(request.POST.get('username')==USERNAME and request.POST.get('password')==PASSWORD):
            data['username'] = request.POST.get('username')
            data['password'] = request.POST.get('password')
            data['saveLogin']=True
            return render(request, 'adminHome.html',data)
        
        else:
            messages.error(request, 'Login Failed ! Please Check your credentials...')
            return render(request, 'login.html')
            
        
        
    
    # data={"username":"admin", "password":"admin"}
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
