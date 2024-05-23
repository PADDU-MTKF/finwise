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

USER_ENDPOINTS={"team":"userTeam.html",
                "project":"userProject.html",
                "details":"userTimeline.html"
                }

COLLECTION={"login":os.getenv('EMPDETAILS_ID'),
            "team":os.getenv('EMPDETAILS_ID'),
            "project":os.getenv('PROJECTS_ID'),
            "project_setting":os.getenv('PROJECT_SETTINGS_ID')
            }

MULTI_DATA={"project":["project","project_setting"]}
USERS_PAGE={'project':'creator','analytics':'username'}

def getPageData(page,refresh=False,query = None,username=""):
    latest_data = {}
    try:
        latest_data=cache.get(page+username) if not refresh else None
        if latest_data is None:
            try:
                # Initialize the base query list
                base_query = [Query.not_equal("userName", [MASTER_ADMIN_USERNAME])]
                # Extend the base query list with the additional query if it's not None
                if query is not None:
                    base_query.extend(query)

                # print(f"1 {page}",base_query)

                latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page] ,base_query)
            except Exception as e:
                # print("2",e)
                # print("3",query)
                try:
                    latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page],query)
                except:
                    latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page])

                
            # print(latest_data)
            cache.set(page+username,latest_data)
            # print("cacheed:",page)
            
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
                if page in MULTI_DATA:
                    for each in MULTI_DATA[page]:
                        data["data" if page == each else each]=getPageData(each)
                else:
                    latest_data=getPageData(page if page is not "" else ADMIN_DEFAULT_PAGE)
                    data["data"]=latest_data
                
                data["page"]=page if page is not "" else ADMIN_DEFAULT_PAGE
                
                try:
                    return render(request, ADMIN_ENDPOINTS[page], data)
                except:
                    return render(request, ADMIN_ENDPOINTS[ADMIN_DEFAULT_PAGE], data)
                    
            else:
                
                if page in MULTI_DATA:
                    for each in MULTI_DATA[page]:
                        try:
                            data["data" if page == each else each]=getPageData(each,query=[
                                      Query.equal(USERS_PAGE[page], [username])] if page in USERS_PAGE else None,username=username)
                        except:
                             data["data" if page == each else each]=getPageData(each)

                else:

                    try:
                        latest_data=getPageData(page if page is not "" else USER_DEFAULT_PAGE,query=[
                                      Query.equal(USERS_PAGE[page], [username])] if page in USERS_PAGE else None,username=username)
                    except:
                        latest_data=getPageData(page if page is not "" else USER_DEFAULT_PAGE)

                    data["data"]=latest_data


                data["page"]=page if page is not "" else ADMIN_DEFAULT_PAGE
                
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
        page="project"
        latest_data={}
        if "adminSave" in request.POST:
            updateData={"title":request.POST.get('title'),
                     "askValue":True if request.POST.get('askValue')=="on" else False,
                     "userLevels":True if request.POST.get('userLevels')=="on" else False
                    }
            
            res=db.updateDocument(os.getenv("DB_ID"),COLLECTION["project_setting"],os.getenv("PROJECT_SETTINGS_DOC_ID"),updateData)
            
            if res:
                messages.success(request, 'Settings Edited Sucessfuly')
            else:
                messages.error(request,"Somthing Went Wrong Try Again...")
                
                
            for each in MULTI_DATA[page]:
                latest_data["data" if page == each else each]=getPageData(each,True)
            
            latest_data['page']=page
                    
            return render(request, ADMIN_ENDPOINTS[page],latest_data)
        
        if "userProSave" in request.POST:
            newData={
                "name":request.POST.get("name"),
                "value":int(request.POST.get("value")) if request.POST.get("value") is not None else 0,
                "deadLine":str(request.POST.get("date")),
                "description":request.POST.get("description"),
                "creator":request.POST.get("creator"),
                "isComplete":False
            }

            res=db.addDocument(os.getenv("DB_ID"),COLLECTION["project"],newData)

            if res:
                 messages.success(request, 'Project Created Sucessfuly')
            else:
                messages.error(request,"Somthing Went Wrong Try Again...")

            
            for each in MULTI_DATA[page]:
                latest_data["data" if page == each else each]=getPageData(each,True,query=[
                                      Query.equal("creator", [request.POST.get("creator")])],username=request.POST.get("creator"))

            latest_data['page']=page   
            return render(request, USER_ENDPOINTS[page],latest_data)

        
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
            # print(type(request.POST.get('phoneNumber')))
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
        return render(request, ADMIN_ENDPOINTS['team'],{"data":latest_data,"page":"team"})
    
    data={"page":"team"}
    return render(request, 'login.html',data)


def analysis(request):
    if request.method == 'POST':
        return render(request, 'adminAnalysis.html')
    
    data={"page":"analysis"}
    return render(request, 'login.html',data)


def details(request):
    if request.method == 'POST':
        project_details={"proid":request.POST.get("proid"),
              "pname":request.POST.get("pname"),
              "pdead":request.POST.get("pdead"),
              "pdes":request.POST.get("pdes"),
              "pcreator":request.POST.get("pcreator"),
              "pcomp":request.POST.get("pcomp")}
        # print(request.POST.get("proid"))
        return render(request, 'userTimeline.html',{"page":"details","project_details":project_details})
    
    data={"page":"details"}
    return render(request, 'login.html',data)
