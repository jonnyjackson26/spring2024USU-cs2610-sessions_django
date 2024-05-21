from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from .models import User, Destination, Session
import hashlib
from .signInFunctions import isValidEmail, isValidPassword
import secrets
from .middleware import session_middleware

# Create your views here.
def index(req):
    #most recent public destinations
    dests=Destination.objects.filter(share_publicly=1).order_by('-id')[:5]
    #add name to each thing
    for d in dests:
        who=User.objects.get(id=int(d.user_id)).name
        d.whoPosted=who

    return render(req,'core/index.html',{"destinations":dests,"topBarInfo":getTopBarInfo(req)})

def signIn(req): #/sessions/new/
    return render(req,'core/signIn.html',{"topBarInfo":getTopBarInfo(req)})

def signInToAccount(req): #/session/ #creates session
    try:
        user = User.objects.get(email=req.POST.get("email"))
        theHash=hashlib.sha1()
        theHash.update(req.POST.get("pw").encode('utf-8'))
        if(user.password_hash==(theHash.hexdigest()+user.salt)):
            #create session
            myToken=secrets.token_urlsafe(32)
            session = Session(
                token=myToken,
                user=User.objects.get(pk=user.id) #these dont need different names do they?
            )
            session.save()
            response=redirect("/destinations")
            response.set_cookie("token",myToken)
            return response
        else:
            return HttpResponseBadRequest("404 Error: bad password.")
    except:
        return HttpResponseBadRequest("404 Error: bad email.")

def signUp(req): #/users/new/
    return render(req,'core/signUp.html',{"topBarInfo":getTopBarInfo(req)})

def createAccount(req):  #/users/
    if(isValidPassword(req.POST.get("pw")) and isValidEmail(req.POST.get("email"))):
        sha1=hashlib.sha1()
        sha1.update(req.POST.get("pw").encode('utf-8')) 
        sal=secrets.token_hex(8)
        user = User(
            name=req.POST.get("name"),
            email=req.POST.get("email"),
            password_hash=sha1.hexdigest()+sal,
            salt=sal

        )
        user.save()

        #create session
        myToken=secrets.token_urlsafe(32)
        session = Session(
            token=myToken,
            user=User.objects.get(pk=user.id) #these dont need different names do they?
        )
        session.save()
        response=redirect("/destinations")
        response.set_cookie("token",myToken)
        return response
    else:
        return HttpResponseBadRequest("400 Error: Make sure your email is not already taken and contains a '@'. Also, your password must be >8 characters and contain a number.")

@session_middleware
def logout(req):
    print("logged out")
    #delete session
    Session.objects.get(token=req.COOKIES.get('token')).delete()
    response=redirect("/")
    #delete cookie
    response.delete_cookie('token')
    return response

@session_middleware
def destinations(req):
    dests=Destination.objects.filter(user_id=req.user.id)
    return render(req, 'core/destinations.html',{"destinations":dests,"topBarInfo":getTopBarInfoLoggedInTho()})

@session_middleware
def givenDestination(req,id): #destinations/<int:id>
    dest=Destination.objects.get(pk=id)
    if dest.user_id==req.user.id:
        return render(req,'core/destination.html',{"destination":dest,"topBarInfo":getTopBarInfoLoggedInTho()})
    else:
        return HttpResponseBadRequest("you dont have accsess")

@session_middleware
def createDestination(req):
    public = req.POST.get("public")=="on"
    destination = Destination(
        name=req.POST.get("name"),
        review=req.POST.get("review"),
        rating=req.POST.get("rating"),
        share_publicly=public,
        user=req.user
    )
    destination.save()
    return redirect("/destinations")

@session_middleware
def deleteDestination(req,id):
    try:
        Destination.objects.get(id=id).delete()
        return redirect("/destinations")
    except: 
        return HttpResponseNotFound()

@session_middleware    
def editDestination(req,id):
    try:
        dest = Destination.objects.get(id=id)
        public = req.POST.get("public")=="on"
        dest.name=req.POST.get("name")
        dest.review=req.POST.get("review")
        dest.rating=int(req.POST.get("rating"))
        dest.share_publicly=public
        dest.save()
        return redirect("/destinations")
    except: 
        print("could not edit your destination")
        return HttpResponseNotFound()

@session_middleware
def renderCreateDestinationPage(req):
    return render(req,'core/createDestination.html',{"topBarInfo":getTopBarInfoLoggedInTho()})




def getTopBarInfo(req):
    topBarInfo=[]
    isLoggedIn=False
    try:
        isLoggedIn= Session.objects.get(token=req.COOKIES.get('token'))!=None
    except:
        pass
    if isLoggedIn: #if logged in
        topBarInfo.append("/destinations/")
        topBarInfo.append("My Destinations")
        topBarInfo.append("/logout/")
        topBarInfo.append("Log out")
    else:  #if not logged in
        topBarInfo.append("/sessions/new/")
        topBarInfo.append("Log in")
        topBarInfo.append("/users/new/")
        topBarInfo.append("Sign up")
    return topBarInfo

def getTopBarInfoLoggedInTho():
    topBarInfo=[]
    topBarInfo.append("/destinations/")
    topBarInfo.append("My Destinations")
    topBarInfo.append("/logout/")
    topBarInfo.append("Log out")
    return topBarInfo
