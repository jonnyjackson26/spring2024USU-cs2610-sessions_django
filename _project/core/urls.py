from django.urls import path,include
from . import views

urlpatterns = [
    path('',view=views.index),
    path('users/new/',view=views.signUp),
    path('sessions/new/',view=views.signIn),
    path('sessions/',view=views.signInToAccount),
    path('logout/',view=views.logout),
    path('users/',view=views.createAccount),
    path('destinations/',view=views.destinations),
    path('destinations/<int:id>/',view=views.givenDestination),
    path('destinations/delete/<int:id>/',view=views.deleteDestination),
    path('destinations/edit/<int:id>/',view=views.editDestination),
    path('destinations/new/',view=views.createDestination),
    path('createDestination/',view=views.renderCreateDestinationPage)
]

