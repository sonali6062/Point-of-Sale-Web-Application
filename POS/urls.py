from django.urls import path
from . import views

urlpatterns=[
    path('staffProfile', views.staffProfile, name='staffProfile'),

    path('takeOrder',views.takeOrder,name='takeOrder'),
    path('getOrder', views.getOrder,name='getOrder'),
    path('deleteOrder', views.deleteOrder,name='deleteOrder'),
    path('manageOrders',views.manageOrders,name='manageOrders'),
    path('manageKOTS',views.manageKOTS,name='manageKOTS'),
    path('manageCustomers',views.manageCustomers,name='manageCustomers'),

    path('logout',views.logout,name='logout'),
]