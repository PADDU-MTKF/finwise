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

COLLECTION={"login":os.getenv('LOGIN_ID'),
            "team":os.getenv('EMPDETAILS_ID')
            }





def getPageData(page):
    latest_data = {}
    try:
        latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page])
    except Exception as e:
        print(f"Error getting Latest Data : {e}")
    
    return latest_data

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
        user_det, _ = db.getDocument(os.getenv('DB_ID'), COLLECTION["login"], [
                                      Query.equal("userName", [username]), Query.equal("password", [pswd])])

        if user_det:
            # Setting user data for rendering templates
            data['username'] = request.POST.get('username')
            data['password'] = request.POST.get('password')
            data['saveLogin'] = True

            # Redirecting to admin or user home page based on user role
            if user_det[0]['isAdmin']:
                latest_data=getPageData(page if page is not "" else ADMIN_DEFAULT_PAGE)
                data["data"]=latest_data
                
                try:
                    return render(request, ADMIN_ENDPOINTS[page], data)
                except:
                    return render(request, ADMIN_ENDPOINTS[ADMIN_DEFAULT_PAGE], data)
                    
            else:
                latest_data=getPageData(page if page is not "" else USER_DEFAULT_PAGE)
                data["data"]=latest_data
                
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
        # can have basic display of all users,add request,edit request,delete request
        '''
        = add mai pop up hoga fir save dabathe he isi end point mai aayega fir db mai save hoga fir naya data ko leke firse adminTeam mai jayega
        = remove mai be same as add
        = edit mai be same as add
        '''
        
        if "add" in request.POST:
            # check for integer and try also make sure sum of all percent pay is <100
            print(request.POST.get('isPercent'))
            newData={"userName":request.POST.get('userName'),
                     "name":request.POST.get('name'),
                     "jobTitle":request.POST.get('jobTitle'),
                     "phoneNumber":request.POST.get('phoneNumber'),
                     "isPercent":True if request.POST.get('isPercent')=="on" else False,
                     "pay":request.POST.get('pay')}
            
            db.addDocument(os.getenv("DB_ID"),COLLECTION["team"],newData)
            #add data to database
            pass
        
        elif "edit" in request.POST:
            # check for integer and try also make sure sum of all percent pay is <100
            updateData={"userName":request.POST.get('userName'),
                     "name":request.POST.get('name'),
                     "jobTitle":request.POST.get('jobTitle'),
                     "phoneNumber":request.POST.get('phoneNumber'),
                     "isPercent":True if request.POST.get('isPercent')=="on" else False,
                     "pay":request.POST.get('pay')}
            
            db.updateDocument(os.getenv("DB_ID"),COLLECTION["team"],request.POST.get('docID'),updateData)
            #edit data to database
            pass
        
        elif "delete" in request.POST:
            db.deleteDocument(os.getenv("DB_ID"),COLLECTION["team"],request.POST.get('docID'))
            #delete data from database
            pass
        else:
            data={"page":"team"}
            return render(request, 'login.html',data)
        

        latest_data=getPageData("team")
        return render(request, ADMIN_ENDPOINTS['team'],{"data":latest_data})
    
    data={"page":"team"}
    return render(request, 'login.html',data)


def finance(request):
    if request.method == 'POST':
        return render(request, 'adminFinance.html')
    
    data={"page":"finance"}
    return render(request, 'login.html',data)


