from .models import Session, User,Destination
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest



def session_middleware(next):
    def middleware(req, *args, **kwargs):
        try:
            token = req.COOKIES.get('token')
            session = Session.objects.get(token=token)
            user=User.objects.get(id=session.user_id)
            req.user=user
            
            #i should prolly check to make sure the logged in user is allowed to access a certain destination.

            response = next(req, *args, **kwargs)
            return response
      
        except:
            return redirect("/sessions/new")
        
        
    return middleware



"""
def session_middleware(next):
    def middleware(req, *args, **kwargs):
        try: #they have a token
            token = req.COOKIES.get('token')
            session = Session.objects.get(token=token)
            user=User.objects.get(id=session.user_id)

            isAuthorizedToAccessPage=True
            uri=req.META['PATH_INFO']
            if "/destinations/" in uri and uri!="/destinations/new/" and uri!="/destinations/":
                num=uri.split('/')[-2]
                try:
                    destination=Destination.objects.get(id=num)
                except Exception as exception:
                    print("couldnt find it sorry buddy. you do seemed to be logged in tho")
                    return HttpResponseBadRequest() #this happens when u use a uri that is no where in the database, for example /destinations/1000/ but you are logged in
                if destination.user_id==user.id:
                    isAuthorizedToAccessPage=True
                else:
                    isAuthorizedToAccessPage=False
            
            if isAuthorizedToAccessPage:
                res=next(req, *args, **kwargs)
                print("the following is the req, which im about to return")
                print(req)
                return res
            else:
                return HttpResponseBadRequest()
        except Exception as e: # theyre not logged in
            print("redirecting u because you tried accessing a page that u cant get to if ur not logged in")
            return redirect("/sessions/new")
        
        
    return middleware

"""