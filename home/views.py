import os
from django.shortcuts import render, HttpResponse, redirect, redirect
from django.contrib import messages
from . import data as db
from appwrite.query import Query
from django.core.cache import cache
import json 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
from datetime import datetime

MASTER_ADMIN_USERNAME="admin"
ADMIN_DEFAULT_PAGE="analysis"
USER_DEFAULT_PAGE="analysis"

ADMIN_ENDPOINTS={"project":"adminProject.html",
                 "team":"adminTeam.html",
                 "details":"userTimeline.html",
                 "analysis":"analysis.html",
                 }

USER_ENDPOINTS={"team":"userTeam.html",
                "project":"userProject.html",
                "details":"userTimeline.html",
                "analysis":"analysis.html",
                }

COLLECTION={"login":os.getenv('EMPDETAILS_ID'),
            "team":os.getenv('EMPDETAILS_ID'),
            "project":os.getenv('PROJECTS_ID'),
            "project_setting":os.getenv('PROJECT_SETTINGS_ID'),
            "project_stages":os.getenv('PROJECT_STAGES'),
            "project_messages":os.getenv('PROJECT_MESSAGES'),
            "project_current_stage":os.getenv('PROJECT_CURRENT_STAGE'),
            "project_workers":os.getenv('PROJECT_WORKERS'),
            "analysis":os.getenv('PROJECTS_ID')


            }

MULTI_DATA={"project":["project","project_setting"],
            "details":["project_messages","project_stages","project_current_stage","project_workers"],
}

USERS_PAGE={'project':'creator','analysis':'creator',"":'creator'}

def getPageData(page,refresh=False,query = None,username="",proid=""):
    latest_data = {}
    try:
        latest_data=cache.get(page+username+proid) if not refresh else None
        if latest_data is None:
            try:
                # Initialize the base query list
                base_query = [Query.not_equal("userName", [MASTER_ADMIN_USERNAME])]
                # Extend the base query list with the additional query if it's not None
                if query is not None:
                    base_query.extend(query)

                # print(f"1 {page}",base_query)

                latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page] ,base_query)
                # print(page,"0")
                

                
            except Exception as e:
                # print("2",e)
                # print("3",query)
                try:
                    latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page],query)
                    # print(page,"1")

                    
                except:
                    latest_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION[page])
                    # print(page,"1")
                    

            
                
            # print(latest_data)
            if(page != "" and page != "analysis" and page!="project" and page!="team"):
                # print("caching")
                cache.set(page+username+proid,latest_data)
            
        if page=="project" or page=="analysis":
            # pprint(latest_data)
            try:
                # print("collectio nmore")
                additional_id,_=db.getDocument(os.getenv("DB_ID"),COLLECTION['project_workers'],[Query.equal("userName", [username])])
                id_list=[""]
                for each in additional_id:
                    id_list.append(each['projectId'])
                # print(id_list)
                
                additional_data,_=db.getDocument(os.getenv("DB_ID"),COLLECTION['project'],[Query.equal("$id", id_list)])
                # print(additional_data)
                latest_data+=additional_data
            except Exception as e:
                print("Could not find",e)
                   
            # print("cacheed:",page)
            
    except Exception as e:
        print(f"Error getting Latest Data : {e}")
    
    return latest_data

# function to handle user logout
def logout(request):
    data = {'logOut': True}
    cache.clear()
    return render(request, 'login.html', data)

def clear_cache(request):
    cache.clear()
    return redirect("logout")

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
                    
                    if page=="" or page=="analysis":
                        totalPro=len(latest_data)
                        
                        data["totalAsCreator"]=0
                        data["totalPro"]=totalPro
                        data["totalPending"]=sum(1 for item in latest_data if not item['isComplete'] )
                        data["totalCompleted"]=totalPro-data["totalPending"]
                        
                        data["nearToDead"]=sorted(latest_data, key=lambda x: datetime.strptime(x['deadLine'], '%Y-%m-%d'))[:5]
                        
                        addon=getPageData("team",username=username,query=[
                                      Query.equal("userName", [username])])
                        data["userDetails"]=addon
                        
                
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
                    except Exception as e:
                        latest_data=getPageData(page if page is not "" else USER_DEFAULT_PAGE)

                    data["data"]=latest_data
                    
                    
                    if page=="" or page=="analysis":
                        totalPro=len(latest_data)
                        
                        data["totalAsCreator"]=sum(1 for item in latest_data if item['creator'] == username)
                        data["totalPro"]=totalPro
                        data["totalPending"]=sum(1 for item in latest_data if not item['isComplete'] )
                        data["totalCompleted"]=totalPro-data["totalPending"]
                        
                        data["nearToDead"]=sorted(latest_data, key=lambda x: datetime.strptime(x['deadLine'], '%Y-%m-%d'))[:5]
                        
                        addon=getPageData("team",username=username,query=[
                                      Query.equal("userName", [username])])
                        data["userDetails"]=addon
                        


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
    
    # print("pro hear")   
    data={"page":"team"}
    return render(request, 'login.html',data)


def analysis(request):

    data={"page":"analysis"}
    return render(request, 'login.html',data)


def details(request):
    if request.method == 'POST':
        project_details={"proid":request.POST.get("proid"),
              "pname":request.POST.get("pname"),
              "pdead":request.POST.get("pdead"),
              "pdes":request.POST.get("pdes"),
              "pcreator":request.POST.get("pcreator"),
              "pcomp":request.POST.get("pcomp"),
              
              "clientName":request.POST.get("clientName"),
              "clientNum":request.POST.get("clientNum"),
              "clientPlace":request.POST.get("clientPlace"),
              }
        
        latest_data={}
        latest_data["project_details"]=project_details
        latest_data["username"]=request.POST.get("username")
       
        for each in MULTI_DATA['details']:
                
                latest_data[each]=getPageData(each,False,proid=request.POST.get("proid"),query=[
                                    Query.equal("projectId", [request.POST.get("proid")]),Query.order_desc("$createdAt"),Query.limit(100)])
                # print("here")
                
        
        latest_data["team"] =getPageData("team",refresh=False)
        
        # Extract user names and ids from the list latest_data["project_workers"]
        b_user_info = {user['userName']: user['id'] for user in latest_data["project_workers"]}
        # print(b_user_info)

        # Create the new list c
        new_team = []
        new_workers = []

        for user in latest_data["team"]:
            user_info = {
                'name': user['name'],
                'userName': user['userName'],
                'jobTitle': user['jobTitle'],
                'isColab': user['userName'] in b_user_info ,
                'id': b_user_info[user['userName']] if user['userName'] in b_user_info else ""
            }
            new_team.append(user_info)
            
            if user['userName'] in b_user_info:
                worker_info = user_info.copy()
                worker_info['id'] = b_user_info[user['userName']]
                new_workers.append(worker_info)

        latest_data["team"] = new_team
        latest_data["project_workers"] = new_workers
        
        # pprint(latest_data["team"])
        # print("\n\n")
        # pprint(latest_data["project_workers"])
        
        
        # print(latest_data)
        latest_data["page"]="details"
                
    
        # print(request.POST.get("proid"))
        return render(request, USER_ENDPOINTS["details"],latest_data)
    
    return redirect("project")


# AJAX response methods below ****************************************************************

def saveStage(request):
    # Your view logic here
    # return render(request, 'mobile.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            project_id = data.get('projectId')
            date = data.get('date')
            title = data.get('title')
            description = data.get('description')
            
            # Process the data here
            # print(f"Project ID: {project_id}")
            
            
            newData={"projectId":project_id,
                     "description":description,
                     "title":title,
                     "date":date}
          
            
            res=db.addDocument(os.getenv("DB_ID"),COLLECTION["project_stages"],newData)

            if res:
                # Respond with a success message
                getPageData("project_stages",True,proid=project_id,query=[
                                    Query.equal("projectId", [project_id]),Query.order_desc("$createdAt"),Query.limit(100)])
                
                return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            
            
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def saveMsg(request):
    # Your view logic here
    # return render(request, 'mobile.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            project_id = data.get('projectId')
            msg = data.get('msg')
            
            # Process the data here
            # print(f"Project ID: {project_id}")
            # print(f"Msg: {msg}")

            newData={"projectId":project_id,
                     "message":msg}
          
            
            res=db.addDocument(os.getenv("DB_ID"),COLLECTION["project_messages"],newData)

            if res:
                # Respond with a success message
                getPageData("project_messages",True,proid=project_id,query=[
                                    Query.equal("projectId", [project_id]),Query.order_desc("$createdAt"),Query.limit(100)])
                
                return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
        except json.JSONDecodeError:
           
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def saveCurrentStage(request):
    # Your view logic here
    # return render(request, 'mobile.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            project_id = data.get('projectId')
            current_stage = data.get('currentStage')
            docId = data.get('docId')
            
            # Process the data here
            # print(f"Project ID: {project_id}")
            # print(f"current_stage: {current_stage}")
            # print(f"docId: {docId}")

            newData={"projectId":project_id,
                     "stage":int(current_stage)}    
          
            
            res=db.updateDocument(os.getenv("DB_ID"),COLLECTION["project_current_stage"],docId,newData)
            
            if res:
                getPageData("project_current_stage",True,proid=project_id,query=[
                                    Query.equal("projectId", [project_id]),Query.order_desc("$createdAt"),Query.limit(100)])
                
                return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            else:
                res=db.addDocument(os.getenv("DB_ID"),COLLECTION["project_current_stage"],newData)

                if res:
                    # Respond with a success message
                    getPageData("project_current_stage",True,proid=project_id,query=[
                                        Query.equal("projectId", [project_id]),Query.order_desc("$createdAt"),Query.limit(100)])
                    
                    return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
        except json.JSONDecodeError:
           
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def updateProDet(request):
    # Your view logic here
    # return render(request, 'mobile.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            creator = data.get('creator')
            project_id = data.get('projectId')
            prodes = data.get('prodes')
            prodead = data.get('prodead')
            cname = data.get('cname')
            cphone = data.get('cphone')
            cplace = data.get('cplace')
            
            
            # Process the data here
            # print(f"Project ID: {project_id}")
           

            newData={"deadLine":prodead,
                     "description":prodes,
                     "clientName":cname,
                     "clientNum":cphone,
                     "clientPlace":cplace,
                     }    
          
            
            res=db.updateDocument(os.getenv("DB_ID"),COLLECTION["project"],project_id,newData)
            
            # print(creator)
                
            if res:
                # Respond with a success message
                getPageData("project",True,query=[
                                      Query.equal("creator", [creator])],username=creator)
                
                return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
        except json.JSONDecodeError:
           
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def updateStageDetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            changed_values = data.get('changedValues')
            project_id = data.get('projectId')

            # Process and update each document
            for doc_id, new_data in changed_values.items():
                res = db.updateDocument(os.getenv("DB_ID"), COLLECTION["project_stages"], doc_id, new_data)

                if not res:
                    return JsonResponse({'status': 'error', 'message': f'Failed to update document {doc_id}'}, status=400)
                
                
            getPageData("project_stages",True,proid=project_id,query=[
                                    Query.equal("projectId", [project_id]),Query.order_desc("$createdAt"),Query.limit(100)])
            
            return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def deleteStage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            doc_id = data.get('docId')
            project_id = data.get('projectId')
            

            # Delete the document
            res = db.deleteDocument(os.getenv("DB_ID"), COLLECTION["project_stages"], doc_id)

            if res:
                getPageData("project_stages",True,proid=project_id,query=[
                                    Query.equal("projectId", [project_id]),Query.order_desc("$createdAt"),Query.limit(100)])
                
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error'}, status=400)

    return JsonResponse({'status': 'error'}, status=405)



def deleteProject(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            doc_id = data.get('projectId')
            

            # Delete the document
            res = db.deleteDocument(os.getenv("DB_ID"), COLLECTION["project"], doc_id)

            if res:
                getPageData("project",True)
                
                
                
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error'}, status=400)

    return JsonResponse({'status': 'error'}, status=405)




def saveCurrentWorkers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            project_id = data.get('projectId')
            workers = data.get('workers')
            
            # pprint(workers)
            for emp in workers:
                if emp['isColab']:
                    newData={
                        'userName':emp['userName'],
                        'projectId':project_id,
                    }
                    res=db.addDocument(os.getenv("DB_ID"),COLLECTION["project_workers"],newData)
                    if not res:
                        return JsonResponse({'status': 'error'}, status=400)
                else:
                    doc_id=emp['id']

                    # Delete the document
                    res = db.deleteDocument(os.getenv("DB_ID"), COLLECTION["project_workers"], doc_id)
                    if not res:
                        return JsonResponse({'status': 'error'}, status=400)

       
            getPageData("project_workers",True,proid=project_id,query=[
                                    Query.equal("projectId", [project_id]),Query.order_desc("$createdAt"),Query.limit(100)])
                
            #     return JsonResponse({'status': 'success'})
            # else:
            #     return JsonResponse({'status': 'error'}, status=400)
            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error'}, status=400)

    return JsonResponse({'status': 'error'}, status=405)

def saveComplete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            comp = data.get('complete')
            project_id = data.get('projectId')
            username = data.get('username')
            
            # print("Project status : ",type(comp))
            
            new_data={
                "isComplete":comp
            }

            # Process and update each document
            # print(username)
           
            res = db.updateDocument(os.getenv("DB_ID"), COLLECTION["project"], project_id, new_data)

            if not res:
                return JsonResponse({'status': 'error', 'message': f'Failed to update document {res}'}, status=400)
            
            getPageData("project",True,query=[
                                      Query.equal("creator", [username])],username=username)
                
                
           
            return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)