import os
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from . import data as db
from appwrite.query import Query


# Create your views here.

USERNAME="hello"
PASSWORD="hi"
def logout(request):
    data={'logOut':True}
    return render(request,'login.html',data)


def login(request):
    if request.method == 'POST':
        data={}
        username=request.POST.get("username")
        pswd=request.POST.get("password")
        page=request.POST.get("page")
        
        userdet,_=db.getDocument(os.getenv('DB_ID'),os.getenv('LOGIN_ID'),[Query.equal("username", [username]), Query.equal("password", [pswd])])
        
        if userdet:
            data['username'] = request.POST.get('username')
            data['password'] = request.POST.get('password')
            data['saveLogin']=True
            
    
            if userdet[0]['isadmin']:
                return render(request, 'adminHome.html',data)

            return render(request, 'userHome.html',data)
        
        messages.error(request, 'Login Failed ! Please Check your credentials...')
        return redirect('login')
        
        
        
    
    # data={"username":"admin", "password":"admin"}
    return render(request, 'login.html')

