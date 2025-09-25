from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from registrations.models import *
import pickle
import numpy as np

# Create your views here.
def index(request):
    return render(request, 'index.html')

def authManager(request):
    if(request.method == 'POST'):
        Restaurant_ID = request.POST['Restaurant_ID']
        Admin_AccessID = request.POST['Admin_AccessID']
        request.session['Restaurant_ID'] = Restaurant_ID
        request.session['Admin_AccessID'] = Admin_AccessID
        restaurantID_set = RestaurantRegistrationTable.objects.all().values('user_id')
        adminID_set = RestaurantRegistrationTable.objects.all().values('Admin_AccessID')
        restaurantID_list = []
        adminID_list = []
        managerAuth_dict = {}
        for i in restaurantID_set:
            restaurantID_list += [(i['user_id'])]
        for i in adminID_set:
            adminID_list += [(i['Admin_AccessID'])]
        n = len(restaurantID_list)
        for i in range(n):
            managerAuth_dict[restaurantID_list[i]] = adminID_list[i]
        if int(Restaurant_ID) not in restaurantID_list:
            messages.info(request,'You are not authorized to register as Manager')
            return redirect('authManager')
        if managerAuth_dict[int(Restaurant_ID)] == Admin_AccessID:
            return render(request, 'RegisterManager.html')
        else:
            messages.info(request,'You are not authorized to register as Manager')
            return redirect('authManager')
    else:
        return render(request, 'AuthorizeManager.html')

def authStaff(request):
    if(request.method == 'POST'):
        Restaurant_ID = request.POST['Restaurant_ID']
        Manager_AccessID = request.POST['Manager_AccessID']
        request.session['Restaurant_ID'] = Restaurant_ID
        request.session['Manager_AccessID'] = Manager_AccessID
        restaurantID_set = ManagerRegistrationTable.objects.all().values('Restaurant_id')
        managerID_set = ManagerRegistrationTable.objects.all().values('Manager_AccessID')
        restaurantID_list = []
        managerID_list = []
        staffAuth_dict = {}
        for i in restaurantID_set:
            restaurantID_list += [(i['Restaurant_id'])]
        for i in managerID_set:
            managerID_list += [(i['Manager_AccessID'])]
        n = len(managerID_list)
        for i in range(n):
            staffAuth_dict[restaurantID_list[i]] = managerID_list[i]
        if int(Restaurant_ID) not in restaurantID_list:
            messages.info(request,'You are not authorized to register as Staff')
            return redirect('authStaff')
        if staffAuth_dict[int(Restaurant_ID)] == Manager_AccessID:
            return render(request, 'RegisterStaff.html')
        else:
            messages.info(request,'You are not authorized to register as Staff')
            return redirect('authStaff')
    else:
        return render(request,'AuthorizeStaff.html')

def registerManager(request):
    if request.method == "POST":
        managerName = request.POST['managerName']
        nameArr=managerName.split(" ")
        managerFirstName=nameArr[0].capitalize()
        managerLastName=nameArr[1].capitalize()
        managerEmail=request.POST['managerEmail']
        managerAddress=request.POST['managerAddress']
        managerContact=request.POST['managerContact']
        managerAccessID=request.POST['managerAccessID']
        password1=request.POST['password1']
        password2=request.POST['password2']
        restaurantID=request.session['Restaurant_ID']
        adminAccessID=request.session['Admin_AccessID']
        
        if password1==password2:
            if User.objects.filter(email=managerEmail).exists():
                messages.info(request,'email already in use')
                return redirect('registerManager')
            else:
                user=User.objects.create_user(username=managerEmail, password=password1, email=managerEmail, first_name=managerFirstName, last_name=managerLastName, address=managerAddress, contact=managerContact, is_restManager = True)
                manager=ManagerRegistrationTable()
                manager.user_id=user.id
                manager.Restaurant_id=restaurantID
                manager.Admin_AccessID=adminAccessID
                manager.Manager_AccessID=managerAccessID
                manager.Manager_Salary = 0
                user.save()
                manager.save()
                return redirect('/')
        else:
            messages.info(request,'password mismatch')
            return redirect('registerManager')

    else:
        return render(request,'RegisterManager.html')

def loginManager(request):
    if request.method == 'POST':
        managerEmail = request.POST['managerEmail']
        managerPassword = request.POST['managerPassword'] 
        user = auth.authenticate(username = managerEmail, 
                                password = managerPassword)
        if user is not None:
            auth.login(request,user)
            return redirect('RMS/managerProfile')
        else:
            messages.info(request,'Enter valid credentials')
            return redirect('loginManager')
    else: 
        return render(request, 'ManagerLogin.html')

def registerStaff(request):
    if request.method == 'POST':
        staffName=request.POST['staffName']
        nameArr=staffName.split(" ")
        staffFirstName=nameArr[0].capitalize()
        staffLastName=nameArr[1].capitalize()
        staffEmail=request.POST['staffEmail']
        staffAddress=request.POST['staffAddress']
        staffContact=request.POST['staffContact']
        staffDesignation=request.POST['designation']
        password1=request.POST['password1']
        password2=request.POST['password2']
        restaurantID=request.session['Restaurant_ID']
        managerAccessID=request.session['Manager_AccessID']

        if password1==password2:
            if User.objects.filter(email=staffEmail).exists():
                messages.info(request,'email already in use')
                return redirect('registerStaff')
            else:
                user=User.objects.create_user(username=staffEmail, password=password1, email=staffEmail, first_name=staffFirstName, last_name=staffLastName, address=staffAddress, contact=staffContact, is_restStaff = True)
                staff=StaffRegistrationTable()
                staff.user_id=user.id
                staff.Restaurant_id=restaurantID
                staff.Manager_AccessID=managerAccessID
                staff.Staff_designation=staffDesignation
                staff.Staff_Salary=0
                user.save()
                staff.save()
                return redirect('/')
        else:
            messages.info(request,'password mismatch')
            return redirect('registerStaff')

    else:
        return render(request, 'RegisterStaff.html')

def loginStaff(request):
    if request.method == 'POST':
        staffEmail = request.POST['staffEmail']
        staffPassword = request.POST['staffPassword'] 
        user = auth.authenticate(username = staffEmail, password = staffPassword)
        if user is not None:
            auth.login(request,user)
            return redirect('POS/staffProfile')
        else:
            messages.info(request,'Enter valid credentials')
            return redirect('loginStaff')
    else: 
        return render(request, 'StaffLogin.html')

def registerAdmin(request):
    if request.method=='POST':
        adminName=request.POST['adminName']
        nameArr=adminName.split(" ")
        adminFirstName=nameArr[0].capitalize()
        adminLastName=nameArr[1].capitalize()
        adminEmail=request.POST['adminEmail']
        adminAddress=request.POST['adminAddress']
        adminContact=request.POST['adminContact']
        restaurantName=request.POST['restaurantName']
        restaurantAddress=request.POST['restaurantAddress']
        adminAccessID=request.POST['adminAccessID']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(email=adminEmail).exists():
                messages.info(request,'email already in use')
                return redirect('registerAdmin')
            else:
                user=User.objects.create_user(username=adminEmail, password=password1, email=adminEmail, first_name=adminFirstName, last_name=adminLastName, address=adminAddress, contact=adminContact, is_restAdmin = True)
                restaurant=RestaurantRegistrationTable()
                restaurant.user_id=user.id
                restaurant.Restaurant_name=restaurantName 
                restaurant.Restaurant_address=restaurantAddress 
                restaurant.Admin_AccessID=adminAccessID
                user.save()
                restaurant.save()
                return redirect('/')
        else:
            messages.info(request,'password mismatch')
            return redirect('registerAdmin')

    else:
        return render(request, 'RegisterAdmin.html')

def loginAdmin(request):
    if request.method == 'POST':
        adminEmail = request.POST['adminEmail']
        adminPassword = request.POST['adminPassword'] 
        user = auth.authenticate(username = adminEmail, password = adminPassword)
        if user is not None:
            auth.login(request,user)
            return redirect('RMS/adminProfile')
        else:
            messages.info(request,'Enter valid credentials')
            return redirect('loginAdmin')
    else: 
        return render(request, 'AdminLogin.html')

def predictRevenue(request):
    model = pickle.load(open('registrations/model_RFR.pkl', 'rb'))
    output = 0
    if request.method=="POST":
        if request.POST['type_FC'] == 'Yes':
            type_FC = 1
        else:
            type_FC = 0
        if request.POST['type_IL'] == 'Yes':
            type_IL = 1
        else:
            type_IL = 0
        if request.POST['type_DT'] == 'Yes':
            type_DT = 1
        else:
            type_DT = 0
        if request.POST['bigCity'] == 'Yes':
            bigCity = 1
        else:
            bigCity = 0
        openTime = int(request.POST['openTime'])
        int_features = [type_FC, type_IL, type_DT, bigCity, openTime]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
        output = round(prediction[0], 2)
    
    toPass={'result':output}
    return render(request, 'revenuePrediction.html',toPass)