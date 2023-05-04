from typing import final
from django import http
from django.db.models.fields import SmallIntegerField
from django.shortcuts import render , redirect

from django.contrib import messages
from django.contrib.auth.models import User, auth

from django.http import HttpResponse
from django.utils.regex_helper import flatten_result

from django.db import connections

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import notfications, post, user , relatives , images_dataset , requests

from datetime import datetime

from deepface import DeepFace
import cv2
import os

from twilio.rest import Client

from sms import send_sms

import pyrebase
 

Config = {
    "apiKey": "AIzaSyBDGebilFj4eqRFGJBJZj7PpkTVMjk7vxw",
    "authDomain": "find-me-753b1.firebaseapp.com",
    "databaseURL": "https://find-me-753b1-default-rtdb.firebaseio.com",
    "projectId": "find-me-753b1",
    "storageBucket": "find-me-753b1.appspot.com",
    "messagingSenderId": "240278123436",
    "appId": "1:240278123436:web:edd1626fe2165022590009",
    "measurementId": "G-H0Z3EEM0P3"
  }



firebase = pyrebase.initialize_app(Config)
storage = firebase.storage()




#{services for testing}#######################################################################################################################################


@csrf_exempt
def test0(request):

    return HttpResponse(to_image("ironman.png"))


@csrf_exempt
def test(request):
    image1 = request.POST['image1']
    image2 = request.POST['image2']

    return HttpResponse(face_recognation(to_image(image1.replace("/","\\")),to_image(image2.replace("/","\\"))))


@csrf_exempt
def test2(request):#done

    account_sid = 'ACdc590e6ac9597a3f5a826c6461b92dd8'
    auth_token = 'a6b9f9a7da207b7273e875cbcd45698b'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            #messaging_service_sid='MG9752274e9e519418a7406176694466fa',
            body='hello again from django gp project , msg 2',
            from_='+12678334007',
            to='+201063491762'
        )

    return HttpResponse("done sms nigga")


@csrf_exempt
def test3(request):

    path = "ironman.png"

    storage.child(path).download("","photos/"+path)
    
    return HttpResponse("done firebase download")


def view(request) :

    val = request.session.get('current_user', 'no session')

    request.session['current_user'] = "5"
    
    return HttpResponse(val)
    #return HttpResponse(request.build_absolute_uri()) 




#{functions}#######################################################################################################################################



def delete_posts(list):

    #for each post id in list
    for post_id in list:

        #delete post that contains that id from the database
        current_post = post.objects.get(id=post_id)

        #delete the image in the folder of this post - to done ----------------------------------------------------------------------


        #delete it
        current_post.delete()


def msg_maker(msg,other_post_id):

    final_msg = msg
    if (other_post_id != None):
        other_post = post.objects.get(id=other_post_id)
        other_user = user.objects.get(id=other_post.user.id)
        post_msg = "\n\n\nusername:" + other_user.user_name + "\nemail:" + other_user.email + "\nphone:" + other_user.phone

        if (other_post.type=='founder'):
            post_msg += "\ndate:" +  other_post.datetime.strftime("%m/%d/%Y, %H:%M:%S") + "\npost location:" + other_post.location

        final_msg += post_msg

    return final_msg


def to_image(image):
    img = os.getcwd() + "/photos/" + image
    return img.replace('/','\\')


def face_recognation(image1,image2):
    img1=cv2.imread(image1)
    img2=cv2.imread(image2)
    result = DeepFace.verify(img1,img2)
    return result["verified"]


def match(image,type):
    #the returned list
    list = []
    posts = None 

    #if type:founder
    if type == 'founder':
        #return all seeker posts
        posts = post.objects.all().filter(type='seeker')


    #if type:seeker
    if type == 'seeker':
        #return all founder posts
        posts = post.objects.all().filter(type='founder')


    #loop at posts
    for current_post in posts:
        
        #if the image simlier to post image
        if(face_recognation(to_image(image),to_image(current_post.image_dir))==True):

            #then add post id to the list
                list.append(current_post.id)


    #return list
    return list


def in_hand_exist(list):
    #loop at list
    for post_id in list:
        #get the post from post_id
        current_post = post.objects.get(id=post_id)

        #if current post is in_hand
        if(current_post.case == 'in hand'):
            return current_post

    #if there is no in_hand
    return None        


def send_notfication(user_id,description):

    notfication = notfications(user = user_id,smallDescription = description ,date = datetime.now())
    notfication.save()


def send_msg(sender,reciver,description):
    account_sid = 'ACdc590e6ac9597a3f5a826c6461b92dd8'
    auth_token = 'a6b9f9a7da207b7273e875cbcd45698b'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            #messaging_service_sid='MG9752274e9e519418a7406176694466fa',
            body=description + "\n\n\nusername:" + sender.user_name + "\nemail:" + sender.email + "\nphone:" + sender.phone,
            from_='+12678334007',
            to= '+2' + reciver.phone
            )

    send_notfication(reciver,description + "\n\n\nusername:" + sender.user_name + "\nemail:" + sender.email + "\nphone:" + sender.phone) #send notfication for reciver        


def session_exist(request,str):
    val = request.session.get(str, '')
    if val == '' or val == None:
        return False
    else:
        return True


def GetUser(user_id):

    #get user of current user id
    the_user = user.objects.get(id=user_id)

    
    json = {
                'user_id':the_user.id,
                'user_name':the_user.user_name,
                'profile_picture':the_user.profile_picture
            }

    return json


def GetPosts(user_id):

    #empty list
    list = []

    #get posts of current user id
    user_posts = post.objects.all().filter(user=user.objects.get(id=user_id))

    #loop
    for current_post in user_posts:
        json = {
                   'post_id':current_post.id,
                   'description':current_post.description ,
                   'datetime' :current_post.datetime.strftime("%m/%d/%Y, %H:%M:%S") ,
                   'image_dir':current_post.image_view
                }

        list.append(json)

    return list  


def GetNotfications(user_id):

    #empty list
    list = []

    #get notfications of current user id
    user_notfications = notfications.objects.all().filter(user=user.objects.get(id=user_id))

    #loop
    for notfication in user_notfications:
        json = {
                    'notfication_id':notfication.id,
                    'smallDescription':notfication.smallDescription,
                    'date':notfication.date.strftime("%m/%d/%Y, %H:%M:%S")
                }

        list.append(json)

    return list  


def GetRelatives(user_id):
    #empty list
    list = []

    #get relatives of current user id
    user_relatives = relatives.objects.all().filter(user=user.objects.get(id=user_id))

    #loop
    for current_relative in user_relatives:
        '''
        json = {
                    'relative_relation_id': current_relative.id,
                    'user': GetUser(current_relative.relative.id)
                }
        '''        

        #list.append(json)
        list.append(GetUser(current_relative.relative.id))

    return list     


def GetRequests(user_id):
    #empty list
    list = []

    #get requests of current user id
    user_requests = requests.objects.all().filter(reciver=user.objects.get(id=user_id))

    #loop
    for current_request in user_requests:
        '''
        json = {
                    'request_id': current_request.id,
                    'user': GetUser(current_request.sender.id)
                }
        '''        

        #list.append(json)
        list.append(GetUser(current_request.sender.id))

    return list   



#{requests}#######################################################################################################################################


#signup , (post)
@csrf_exempt
def SignUp(request): #done

    if request.method == 'POST':

        #0-variables
        ok = True
        msg = "" 

        #1-get parameters of post
        post_user_name  = request.POST['user_name']
        post_password  = request.POST['password']
        post_email  = request.POST['email']
        post_phone  = request.POST['phone']

        #2-checking (sql)


        if user.objects.all().filter(email=post_email).exists():
            msg += "email taken|"
            ok = False           

        if user.objects.all().filter(phone=post_phone).exists():
            msg += "phone taken|"
            ok = False 

        if post_user_name == "" or post_password == "" or post_email == "" or post_phone == "" :
            msg += "no field can be empty|"
            ok = False  



        #3-insert in database
        if(ok==True):

            current_user = user(user_name=post_user_name , password=post_password , email=post_email , phone=post_phone)
            current_user.save()

            request.session['current_user'] = current_user.id

            #return json 
            json = {
                    "error":False,
                    "user_id": current_user.id,
                    "user_name" : current_user.user_name ,
                    "password" : current_user.password ,
                    "email" : current_user.email ,
                    "profile_picture" : current_user.profile_picture ,
                    "location" : current_user.location ,
                    "phone" : current_user.phone ,
                    "posts" : GetPosts(current_user.id),
                    "notfications" : GetNotfications(current_user.id),
                    "relatives": GetRelatives(current_user.id),
                    "requests": GetRequests(current_user.id),
                }

            return JsonResponse(json)

        #4-return msg
        return JsonResponse({"error":True,   "msg" : msg})

    return JsonResponse({"error":True,   "msg" :'(signup) not post method!!!'})  


#login , (post)
@csrf_exempt
def LogIn(request): #done

    if request.method == 'POST':

        if session_exist(request,'current_user'):
            return JsonResponse({"error":True,   "msg" :'current user already logged in !!!'})

        else:    
            #1-get parameters of post
            post_email  = request.POST['email']
            post_password  = request.POST['password']

            #2-checking (sql)
            if user.objects.all().filter(email=post_email,password=post_password).exists() :

                #take the current account 
                current_user = user.objects.get(email=post_email,password=post_password)

                #sessions 
                #request.session['current_user'] = current_user.id

                #return json 
                json = {
                    "error":False,
                    "user_id": current_user.id,
                    "user_name" : current_user.user_name ,
                    "password" : current_user.password ,
                    "email" : current_user.email ,
                    "profile_picture" : current_user.profile_picture ,
                    "location" : current_user.location ,
                    "phone" : current_user.phone ,
                    "posts" : GetPosts(current_user.id),
                    "notfications" : GetNotfications(current_user.id),
                    "relatives": GetRelatives(current_user.id),
                    "requests": GetRequests(current_user.id),   
                }


                #3-return msg
                return JsonResponse(json)
     

            else:
                return JsonResponse({"error":True,   "msg" :'invaild inputs , check email and password !!!'})    

    return JsonResponse({"error":True,   "msg" :'(login) not post method!!!'})


#logout , (get)
@csrf_exempt
def LogOut(request): #ok

    if request.method == 'GET':
        if session_exist(request,'current_user'):
            del request.session['current_user']
            return JsonResponse({"error":False,   "msg" :'logout done!!!'})
            
        else:
            return JsonResponse({"error":True,   "msg" :'no current user!!!'}) 
            
    else:
         return JsonResponse({"error":True,   "msg" :'(logout) not get method!!!'})      


#edit user , (post)
@csrf_exempt
def EditProfile(request): #ok
    if request.method == 'POST':

        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):


            #1-get parameters of post
            post_user_name  = request.POST.get('user_name',None)
            post_password  = request.POST.get('password',None)
            post_phone = request.POST.get('phone',None)
            post_location = request.POST.get('location',None)
            post_image_profile = request.POST.get('image_profile',None)

            #2-load the current user from database
            current_user = user.objects.get(id=request.session['current_user'])

            #3-change variables with ternary operator
            current_user.user_name =  post_user_name if (post_user_name != None and post_user_name != "") else current_user.user_name
            current_user.password =  post_password if (post_password != None and post_password != "") else current_user.password
            current_user.phone =  post_phone if (post_phone != None and post_phone != "") else current_user.phone
            current_user.location =  post_location if (post_location != None and post_location != "") else current_user.location
            current_user.profile_picture =  post_image_profile if (post_image_profile != None and post_image_profile != "") else current_user.profile_picture

            #download the image

            storage.child(current_user.profile_picture).download("","photos/"+current_user.profile_picture)

            #4-save
            current_user.save()
            return JsonResponse({"error":False,   "msg" :'user info updated!!!!!!'})

        else:
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'}) 

    return JsonResponse({"error":True,   "msg" :'(EditProfile) not post method!!!'})

#SearchUser , (post)
@csrf_exempt
def SearchUser(request): #ok
    if request.method == 'POST':
        
        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):

            list = []

            #get username of post method
            username = request.POST.get("username")

            #get notfications of current user id
            users = user.objects.all().filter(user_name__icontains=username)

            #loop
            for current_user in users:
                if str(current_user.id) != request.session['current_user'] : #if not me

                    json = {
                            'user_id':current_user.id,
                            'user_name':current_user.user_name,
                            'email':current_user.email,
                            'profile_picture':current_user.profile_picture,
                            'location':current_user.location,
                            'phone':current_user.phone,
                    }

                    list.append(json)

            
            final_json = {
                'error':False,
                'users':list
            }   


            return JsonResponse(final_json) 

        else:#done
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'})  

    else:#done
        return JsonResponse({"error":True,   "msg" :'(SearchUser) not post method!!!'})

#deleterelative , (post)
@csrf_exempt
def DeleteRelative(request): #ok
    if request.method == 'POST':

        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):

            #get the relative id from post method
            relative_id = request.POST.get("relative_id")
            
            #get relatives of current user id
            user_relatives = relatives.objects.all().filter(user=user.objects.get(id=request.session['current_user']))

            #list=[]

            #loop at user relatives and see if the relative id of user_relatives equals the relative id of post method
            for current_relative in user_relatives :
                if str(current_relative.relative.id) == relative_id :
                    current_relative.delete()
                    relatives.objects.get(user=user.objects.get(id=relative_id),relative=user.objects.get(id=request.session['current_user'])).delete()
                    return JsonResponse({"error":False,   "msg" :'relative deleted!!!!!!'}) 


            return JsonResponse({"error":True,   "msg" :'no relative with this id!!!!!!'})      

        else:#done
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'})  

    else:#done
        return JsonResponse({"error":True,   "msg" :'(deleterelatives) not post method!!!'}) 

#deleterequest , (post)
@csrf_exempt
def DeleteRequest(request): #ok
    if request.method == 'POST':
        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):

            #get the sender id from post method
            sender_id = request.POST.get("sender_id")
            
            #get requests of current user id
            user_requests = requests.objects.all().filter(reciver=user.objects.get(id=request.session['current_user']))

            #list=[]

            #loop at user relatives and see if the relative id of user_relatives equals the relative id of post method
            for current_request in user_requests :
                if str(current_request.sender.id) == sender_id :
                    current_request.delete()
                    return JsonResponse({"error":False,   "msg" :'request deleted!!!!!!'})
                    

            return JsonResponse({"error":True,   "msg" :'no request with this id!!!!!!'})     

        else:#done
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'})


    else:#done
        return JsonResponse({"error":True,   "msg" :'(deleterequest) not post method!!!'}) 

#confirmrequest , (post)
@csrf_exempt
def ConfirmRequest(request): #ok
    if request.method == 'POST':
        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):

            #get the sender id from post method
            sender_id = request.POST.get("sender_id")
            
            #get requests of current user id
            user_requests = requests.objects.all().filter(reciver=user.objects.get(id=request.session['current_user']))

            #list=[]

            #loop at user relatives and see if the relative id of user_relatives equals the relative id of post method
            for current_request in user_requests :
                if str(current_request.sender.id) == sender_id :
                    relatives(user=user.objects.get(id=sender_id),relative=user.objects.get(id=request.session['current_user'])).save()  #add new relative to the database
                    relatives(user=user.objects.get(id=request.session['current_user']),relative=user.objects.get(id=sender_id)).save()  #mirror
                    send_notfication(user.objects.get(id=sender_id),user.objects.get(id=request.session['current_user']).user_name+" accepted your relative request!!!")
                    
                    current_request.delete()
                    return JsonResponse({"error":False,   "msg" :'request confirmed!!!!!!'})
                    

            return JsonResponse({"error":True,   "msg" :'no request with this id!!!!!!'})    


        else:#done
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'}) 

    else:#done
        return JsonResponse({"error":True,   "msg" :'(confirmrequest) not post method!!!'})  
        
#adduser , (post)
@csrf_exempt
def AddUser(request): #ok
    if request.method == 'POST':
        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):

            #get the user id from post method
            user_id = request.POST.get("add_user_id")

            #check that user id is not himself and user exist and relative not exist
            if(
             user_id!=str(request.session['current_user'])
             and
             user.objects.all().filter(id=user_id).exists()
             and
             not relatives.objects.all().filter(user=user.objects.get(id=request.session['current_user']),relative=user.objects.get(id=user_id)).exists()
             and
             not requests.objects.all().filter(sender=user.objects.get(id=request.session['current_user']),reciver=user.objects.get(id=user_id)).exists()
             and
             not requests.objects.all().filter(sender=user.objects.get(id=user_id),reciver=user.objects.get(id=request.session['current_user'])).exists()
             ) :
             
             
                requests(sender=user.objects.get(id=request.session['current_user']),reciver=user.objects.get(id=user_id)).save()   #create request in database
                send_notfication(user.objects.get(id=user_id),user.objects.get(id=request.session['current_user']).user_name+" send a relative request to you , check it in your profile page!!!") #send notfication for reciver
                return JsonResponse({"error":False,   "msg" :'request sent!!!!!!'})
                

            else :
                return JsonResponse({"error":True,   "msg" :'invalid user id!!!!!!'}) 

        else:#done  
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'})

    else:#done
        return JsonResponse({"error":True,   "msg" :'(adduser) not post method!!!'}) 

#deletepost , (post)
@csrf_exempt
def DeletePost(request): #ok
    if request.method == 'POST':
        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):

            #get the post id from post method
            post_id = request.POST.get("post_id")
            
            #get posts of current user id
            user_posts = post.objects.all().filter(user=user.objects.get(id=request.session['current_user']))

            #loop at user posts and see if the post id of user_posts equals the post id of post method
            for current_post in user_posts :
                if str(current_post.id) == post_id :
                    current_post.delete()
                    return JsonResponse({"error":False,   "msg" :'post deleted!!!!!!'})


            return JsonResponse({"error":True,   "msg" :'no post with this id!!!!!!'})     

        else:#done 
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'}) 

    else:#done
        return JsonResponse({"error":True,   "msg" :'(deletepost) not post method!!!'}) 

#addpost , (post)
@csrf_exempt
def AddPost(request): #ok

    if request.method == 'POST':
        request.session['current_user']=request.POST.get('user_id',None)
        if session_exist(request,'current_user'):

            #take attributes
            post_type  = request.POST['type'].lower()
            post_image  = request.POST['image']
            post_location  = request.POST['location']
            post_description = request.POST.get('description')
            post_case = request.POST.get('case').lower()


            #download the image
            storage.child(post_image).download("","photos/"+post_image)
            

            #check type
            if post_type != 'seeker' and post_type != 'founder':#done
                return JsonResponse({"error":True,   "msg" :'please enter valid type (seeker or founder)!!!!!!'+post_type})

            #create date attribute
            post_date = datetime.now()

            #addpost to database
            current_post = post(type=post_type , image_dir=post_image , location=post_location , description=post_description , case=post_case , datetime=post_date , user=user.objects.get(id=request.session['current_user']))
            current_post.save()

            #matching
            #condition for seeker or founder

            #return HttpResponse(to_image(post_image))

            match_list = match(post_image,post_type) #post ids

            
            #seeker
            if post_type == 'seeker':#done

                #if match
                if (len(match_list)>0):#done

                    is_in_hand = in_hand_exist(match_list) #post

                    #with at least one case in hand
                    if(is_in_hand != None): #done
                        #send notfication for all
                        
                        send_notfication(user.objects.get(id=request.session['current_user']),msg_maker("Match Found! here are the finder details: \n",is_in_hand.id)) #seeker user (newer)
                        send_notfication(is_in_hand.user,msg_maker("Post Matched! Thank you for your help, Seeker will contact you soon. here are the seeker details: \n",current_post.id)) #in_hand founder user (older)

                        #delete posts of all match list + current_post
                        delete_posts(match_list+[current_post.id])       


                    #with no case in hand
                    else: #done
                        #send notfication for seeker for each post
                        for post_id in match_list :
                            
                            send_notfication(user.objects.get(id=request.session['current_user']),msg_maker("Match Found! the following user has seen the missing person. here are his details : \n",post_id)) #seeker user (newer)

                #else 
                else:#done
                    #send notfication for seeker
                    send_notfication(user.objects.get(id=request.session['current_user']),msg_maker("we did not found any match yet , but we will keep you with updates if anything new happend \n",None))


                return JsonResponse({"error":False,   "msg" :'done (seeker case)'})

            #founder
            if post_type == 'founder':#done

                #case : in hand
                if post_case == 'in hand' :#done

                    #if match  -> send notfication for all , delete posts
                    if (len(match_list)>0):#done

                        #send notfication for all
                        send_notfication(user.objects.get(id=request.session['current_user']),msg_maker("Post Matched! Thank you for your help, Seeker will contact you soon. here are the seeker details: \n",match_list[0])) #founder user (newer)
                        send_notfication(post.objects.get(id=match_list[0]).user,msg_maker("Match Found! here are the finder details: \n",current_post.id)) #seeker user (older)

                        #delete posts of all match list + current_post
                        delete_posts(match_list+[current_post.id]) 

                    #else ->  add post in database
                    else:#done
                        #send notfication for founder
                        send_notfication(user.objects.get(id=request.session['current_user']),msg_maker("we did not found any match yet , but we will keep you with updates if anything new happend \n",None))

                #case : kiddnaped
                if post_case == 'kiddnaped' :#done
                    #if match  -> send notfication for seeker
                    if (len(match_list)>0):
                        #send notfication for seeker
                        send_notfication(post.objects.get(id=match_list[0]).user,msg_maker("Match Found! here are the finder details: \n",current_post.id)) #seeker user (older)
                        
                    #send notfication for founder
                    send_notfication(user.objects.get(id=request.session['current_user']),msg_maker("thank you for your help \n",None))

                return JsonResponse({"error":False,   "msg" :'done (founder case)'})         


        else:#done
            return JsonResponse({"error":True,   "msg" :'no current user!!!!!!'})    

    else: #done
        return JsonResponse({"error":True,   "msg" :'(AddPost) not post method!!!'}) 

#saveme , (get)
@csrf_exempt
def SaveMe(request):

    if request.method == 'GET':
        if session_exist(request,'current_user'):
            
            #get all its relatives 
            all_relatives = relatives.objects.all().filter(user=user.objects.get(id=request.session['current_user']))

            #for each one send msg on its with some contact
            for current_relative in all_relatives:
                send_msg(user.objects.get(id=request.session['current_user']),current_relative.relative,"save me please , i am in danger!!!!")

            return HttpResponse('saveme done!!!')    

        else:
            return HttpResponse('no current user!!!')

    else:
         return HttpResponse('(SaveMe) not get method!!!')    

