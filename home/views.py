from django.shortcuts import render,HttpResponse
from django.contrib import messages


# Create your views here.

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