from django.urls import path
from . import views

urlpatterns = [
    
    path('test0/',views.test0 , name='test0'),
    path('test/',views.test , name='test'),
    path('test2/',views.test2 , name='test2'),
    path('test3/',views.test3 , name='test3'),
    path('view/',views.view , name='view'),

    path('LogIn/',views.LogIn , name='LogIn'),
    path('SignUp/',views.SignUp , name='SignUp'),
    path('LogOut/',views.LogOut , name='LogOut'),
    path('EditProfile/',views.EditProfile , name='EditProfile'),
    path('SearchUser/',views.SearchUser , name='SearchUser'),
    path('DeleteRelative/',views.DeleteRelative , name='DeleteRelative'),
    path('DeleteRequest/',views.DeleteRequest , name='DeleteRequest'),
    path('ConfirmRequest/',views.ConfirmRequest , name='ConfirmRequest'),
    path('AddUser/',views.AddUser , name='AddUser'),
    path('DeletePost/',views.DeletePost , name='DeletePost'),
    path('AddPost/',views.AddPost , name='AddPost'),
    path('SaveMe/',views.SaveMe , name='SaveMe'), 
    

] 
