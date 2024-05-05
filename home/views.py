import os
from django.shortcuts import render, HttpResponse, redirect, redirect
from django.contrib import messages
from . import data as db
from appwrite.query import Query
from django.core.cache import cache


MASTER_ADMIN_USERNAME="admin"
ADMIN_DEFAULT_PAGE="team"
USER_DEFAULT_PAGE="team"

ADMIN_ENDPOINTS={"project":"adminProject.html",
                 "team":"adminTeam.html",
                 "analysis":"adminAnalysis.html",
                 }

USER_ENDPOINTS={"team":"userHome.html"}

COLLECTION={"login":os.getenv('EMPDETAILS_ID'),
            "team":os.getenv('EMPDETAILS_ID'),
            "project":os.getenv('PROJECTS_ID')
            }




def getPageData(page,refresh=False):
    latest_data = {}
    try:
        latest_data=cache.get(page) if not refresh else None
        if latest_data is None:
            latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page])
            # latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page] ,[
            #                           Query.not_equal("userName", [MASTER_ADMIN_USERNAME])])
            cache.set(page,latest_data)
            print("cacheed:",page)
            
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
                print(latest_data)
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
            print(type(request.POST.get('phoneNumber')))
            newData={"userName":request.POST.get('userName'),
                     "name":request.POST.get('name'),
                     "jobTitle":request.POST.get('jobTitle'),
                     "phoneNumber":int(request.POST.get('phoneNumber')),
                     "isPercent":True if request.POST.get('isPercent')=="on" else False,
                     "pay":int(request.POST.get('pay')),
                     "password":request.POST.get('password'),
                     "isAdmin":False}
          
            
            res=db.addDocument(os.getenv("DB_ID"),COLLECTION["team"],newData)
            
            if res:
                 messages.success(request, 'User Created Sucessfuly')
            else:
                messages.error(request,"Somthing Went Wrong Try Again...")
                
            
        
        elif "edit" in request.POST:
            # check for integer and try also make sure sum of all percent pay is <100
            updateData={"userName":request.POST.get('userName'),
                     "name":request.POST.get('name'),
                     "jobTitle":request.POST.get('jobTitle'),
                     "phoneNumber":int(request.POST.get('phoneNumber')),
                     "isPercent":True if request.POST.get('isPercent')=="on" else False,
                     "pay":int(request.POST.get('pay')),
                     "password":request.POST.get('password'),
                     "isAdmin":False}
            
            res=db.updateDocument(os.getenv("DB_ID"),COLLECTION["team"],request.POST.get('docID'),updateData)
            
            if res:
                 messages.success(request, 'Data Edited Sucessfuly')
            else:
                messages.error(request,"Somthing Went Wrong Try Again...")
                
            
            #edit data to database
            pass
        
        elif "delete" in request.POST:
            
            res=db.deleteDocument(os.getenv("DB_ID"),COLLECTION["team"],request.POST.get('docID'))
            
            if res:
                 messages.success(request, 'Data Deleted Sucessfuly')
            else:
                messages.error(request,"Somthing Went Wrong Try Again...")
                
            #delete data from database
            pass
        else:
            data={"page":"team"}
            return render(request, 'login.html',data)
        

        latest_data=getPageData("team",refresh=True)
        return render(request, ADMIN_ENDPOINTS['team'],{"data":latest_data})
    
    data={"page":"team"}
    return render(request, 'login.html',data)


def analysis(request):
    if request.method == 'POST':
        return render(request, 'adminAnalysis.html')
    
    data={"page":"analysis"}
    return render(request, 'login.html',data)


