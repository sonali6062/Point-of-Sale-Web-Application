from django.urls import path
from . import views

urlpatterns=[
    path('adminProfile', views.adminProfile, name='adminProfile'),
    path('managerProfile', views.managerProfile, name='managerProfile'),

    path('manageStaff',views.manageStaff,name='manageStaff'),
    path('manageInventory',views.manageInventory,name='manageInventory'),
    path('customizeMenu',views.customizeMenu,name='customizeMenu'),
    path('manageRecipe',views.manageRecipe,name='manageRecipe'),
    path('manageCovers',views.manageCovers,name='manageCovers'),
    path('manageEmployees',views.manageEmployees,name='manageEmployees'),
    
    path('salesRecords',views.salesRecords,name='salesRecords'),
    path('salesAnalysis', views.salesAnalysis,name='salesAnalysis'),

    path('logout',views.logout,name='logout'),
]