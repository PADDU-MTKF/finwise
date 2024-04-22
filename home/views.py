import os
from django.shortcuts import render, HttpResponse, redirect, redirect
from django.contrib import messages
from . import data as db
from appwrite.query import Query

ADMIN_DEFAULT_PAGE="team"
USER_DEFAULT_PAGE="home"

ADMIN_ENDPOINTS={"project":"adminProject.html",
                 "team":"adminTeam.html",
                 "finance":"adminFinance.html",
                 }

USER_ENDPOINTS={"home":"userHome.html"}




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
                                      Query.equal("userName", [username]), Query.equal("password", [pswd])])

        if user_det:
            # Setting user data for rendering templates
            data['username'] = request.POST.get('username')
            data['password'] = request.POST.get('password')
            data['saveLogin'] = True

            # Redirecting to admin or user home page based on user role
            if user_det[0]['isAdmin']:
                try:
                    return render(request, ADMIN_ENDPOINTS[page], data)
                except:
                    return render(request, ADMIN_ENDPOINTS[ADMIN_DEFAULT_PAGE], data)
                    
            else:
                try:
                    return render(request, USER_ENDPOINTS[page], data)
                except:
                    return render(request, USER_ENDPOINTS[USER_DEFAULT_PAGE], data)
                

        # If login fails, display error message and redirect to login page
        messages.error(request, 'Login Failed ! Please Check your credentials...')
        return redirect('login')

    # If request method is not POST, render login page
    return render(request, 'login.html')




def project(request):
    if request.method == 'POST':
        return render(request, 'adminProject.html')
        
    data={"page":"project"}
    return render(request, 'login.html',data)


def team(request):
    if request.method == 'POST':
        return render(request, 'adminTeam.html')
    
    data={"page":"team"}
    return render(request, 'login.html',data)


def finance(request):
    if request.method == 'POST':
        return render(request, 'adminFinance.html')
    
    data={"page":"finance"}
    return render(request, 'login.html',data)


