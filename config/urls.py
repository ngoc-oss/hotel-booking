from django.contrib import admin
from django.urls import path,include
from booking import views as v
urlpatterns=[path('',v.home,name='home'),path('admin/',admin.site.urls),path('accounts/',include('django.contrib.auth.urls')),path('signup/',v.signup,name='signup'),path('rooms/<int:pk>/book/',v.reserve,name='reserve'),path('bookings/',v.mine,name='mine'),path('bookings/<int:pk>/cancel/',v.cancel,name='cancel'),path('health/',v.health),path('metrics',v.metrics)]
