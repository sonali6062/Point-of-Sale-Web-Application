from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='home'),

    path('authManager', views.authManager, name='authManager'),
    path('registerManager', views.registerManager, name='registerManager'),
    path('loginManager', views.loginManager, name='loginManager'),

    path('authStaff', views.authStaff, name='authStaff'),
    path('registerStaff', views.registerStaff, name='registerStaff'),
    path('loginStaff', views.loginStaff, name='loginStaff'),

    path('registerAdmin', views.registerAdmin, name='registerAdmin'),
    path('loginAdmin', views.loginAdmin, name='loginAdmin'),

    path('predictRevenue', views.predictRevenue,name='predictRevenue'),

]
