import os
from django.shortcuts import render, HttpResponse, redirect, redirect
from django.contrib import messages
from . import data as db
from appwrite.query import Query


ADMIN_ENDPOINTS={"home":"adminHome.html","temp":"temp.html"}
USER_ENDPOINTS={"home":"userHome.html"}
def temp(request):
    if request.method=="POST":
        if 'team' in request.POST:
            return redirect('team_view')
        if 'finance' in request.POST:
            return redirect('finance_view')
        if 'work' in request.POST:
            return redirect('work_view')
    return render(request, 'adminHome.html')



# function to handle user logout
def logout(request):
    data = {'logOut': True}
    return render(request, 'login.html', data)

# function to handle user login
def login(request):
    if request.method == 'POST':
        data = {}
        
        # accessing the form details
        username = request.POST.get("username")
        pswd = request.POST.get("password")
        page = request.POST.get("page")

        # Querying the database for user details
        user_det, _ = db.getDocument(os.getenv('DB_ID'), os.getenv('LOGIN_ID'), [
                                      Query.equal("username", [username]), Query.equal("password", [pswd])])

        if user_det:
            # Setting user data for rendering templates
            data['username'] = request.POST.get('username')
            data['password'] = request.POST.get('password')
            data['saveLogin'] = True

            # Redirecting to admin or user home page based on user role
            if user_det[0]['isadmin']:
                try:
                    return render(request, ADMIN_ENDPOINTS[page], data)
                except:
                    return render(request, ADMIN_ENDPOINTS["home"], data)
                    
            else:
                try:
                    return render(request, USER_ENDPOINTS[page], data)
                except:
                    return render(request, USER_ENDPOINTS["home"], data)
                

        # If login fails, display error message and redirect to login page
        messages.error(request, 'Login Failed ! Please Check your credentials...')
        return redirect('login')

    # If request method is not POST, render login page
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
