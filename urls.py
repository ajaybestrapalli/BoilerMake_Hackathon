from django.contrib import admin
from django.urls import path
from hackapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signupuser/',views.signupuser, name='signupuser'),
    path('logoutuser/',views.logoutuser, name='logoutuser'),
    path('loginuser/',views.loginuser, name='loginuser'),

    path('mail/', views.mail, name='mail'),
    path('event/', views.event, name='event'),
    path('checkin/<str:eventname>/', views.checkin, name='checkin'),
]
