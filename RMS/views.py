from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from django.contrib import messages
from registrations.models import *
from RMS.models import*
from POS.models import*
from django.http import JsonResponse
from .utils import getPlot
import json


# Create your views here.
def adminProfile(request):
    restDetails = RestaurantRegistrationTable.objects.filter(user_id=request.user.id)
    adminDetails = User.objects.filter(username = request.user.username)
    return render(request,'adminPage.html',{'details':restDetails, 'Adetails':adminDetails})

def managerProfile(request):
    manager = ManagerRegistrationTable.objects.filter(user_id = request.user.id)
    Manager_AccessID = manager[0].Manager_AccessID
    Restaurant_ID = manager[0].Restaurant_id
    restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
    managerDetails = User.objects.filter(username = request.user.username)
    toPass = {'Restaurantdetails':restDetails,'Managerdetails':managerDetails,'Manager_AccessID':Manager_AccessID}
    return render(request,'managerPage.html', toPass)

def manageStaff(request):
    manager = ManagerRegistrationTable.objects.filter(user_id=request.user.id)
    Restaurant_ID = manager[0].Restaurant_id
    Manager_AccessID = manager[0].Manager_AccessID
    if request.method == 'POST':
        staffName=request.POST['staffName']
        nameArr=staffName.split(" ")
        staffFirstName=nameArr[0]
        staffLastName=nameArr[1]
        staffEmail=request.POST['staffEmail']
        staffAddress=request.POST['staffAddress']
        staffContact=request.POST['staffContact']
        staffDesignation=request.POST['designation']
        staffSalary=request.POST['staffSalary']

        if User.objects.filter(email=staffEmail).exists():
            messages.info(request,'email already in use')
            return redirect('manageStaff')
        else:
            user=User.objects.create_user(username=staffEmail, email=staffEmail, first_name=staffFirstName, last_name=staffLastName, address=staffAddress, contact=staffContact, is_restStaff = True)
            staff=StaffRegistrationTable()
            staff.user_id=user.id
            staff.Restaurant_id=Restaurant_ID
            staff.Manager_AccessID=Manager_AccessID
            staff.Staff_designation=staffDesignation
            staff.Staff_Salary=staffSalary
            user.save()
            staff.save()
            return redirect('manageStaff')
    else:
        restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
        staffSet = StaffRegistrationTable.objects.filter(Restaurant_id=Restaurant_ID)
        staffList=[]
        for staff in staffSet:
            user = User.objects.filter(id=staff.user_id)
            userDetails={
                'name':user[0].first_name.capitalize()+" "+user[0].last_name.capitalize(),
                'designation':staff.Staff_designation,
                'email':user[0].email,
                'address':user[0].address,
                'contact':user[0].contact,
                'salary':staff.Staff_Salary
                }
            staffList.append(userDetails)
        toPass={'staffList':staffList, 'Restaurantdetails':restDetails}
        return render(request, "staffManagement.html", toPass)

def manageInventory(request):
    manager = ManagerRegistrationTable.objects.filter(user_id=request.user.id)
    Restaurant_ID = manager[0].Restaurant_id
    if request.method=='POST':
        ingredientName=request.POST['ingredientName']
        ingredientQuantity=request.POST['ingredientQuantity']
        ingredientPrice=request.POST['ingredientPrice']
        ingrdientPPG=float(ingredientQuantity)/float(ingredientPrice)
        inventory = InventoryTable()
        inventory.Ingredient_Name = ingredientName
        inventory.Inventory_Quantity = ingredientQuantity
        inventory.Ingredient_Price = ingredientPrice
        inventory.Ingredient_PricePerGram = round(ingrdientPPG, 2)
        inventory.Restaurant_id = Restaurant_ID
        inventory.save()
        return redirect('manageInventory')
    else:
        restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
        ingredients = InventoryTable.objects.filter(Restaurant_id=Restaurant_ID)
        toPass={'Restaurantdetails':restDetails,'Ingredients':ingredients}
        return render(request,"inventoryManagement.html", toPass)

def customizeMenu(request):
    manager = ManagerRegistrationTable.objects.filter(user_id=request.user.id)
    Restaurant_ID = manager[0].Restaurant_id
    recipe = False
    if request.method=='POST':
        itemName = request.POST['itemName']
        itemCategory = request.POST['itemCategory']
        itemType = request.POST['itemType']
        itemProfit = request.POST['itemProfitMargin']
        if itemCategory == 'food item':
            itemGst = 5
        else:
            itemGst = 0

        menu = MenuItemsTable()
        menu.Item_Name = itemName
        menu.Item_Category = itemCategory
        menu.Item_Type = itemType
        menu.Item_GST = itemGst
        menu.Item_ProfitMargin = itemProfit
        menu.Restaurant_id = Restaurant_ID
        menu.Cost_Price = 0
        menu.Selling_Price = 0
        menu.save()
        return redirect("customizeMenu")
    else:
        menuList = MenuItemsTable.objects.filter(Restaurant_id = Restaurant_ID)
        restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
        toPass={'Restaurantdetails':restDetails, 'items':menuList, 'recipe':recipe}
        return render(request,"menuCustomization.html", toPass)

def manageRecipe(request):
    manager = ManagerRegistrationTable.objects.filter(user_id=request.user.id)
    Restaurant_ID = manager[0].Restaurant_id
    recipeList = RecipeRequirementsTable.objects.filter(Restaurant_id=Restaurant_ID)

    if  request.method == 'POST':
        ingredientList = {}
        recievedData = json.loads(request.body)
        ItemId = recievedData.get('itemId')
        ingredientName = recievedData.get('ingredientName')
        ingredientQuantity = recievedData.get('ingredientQuantity')
        ingredient = InventoryTable.objects.filter(Restaurant_id=Restaurant_ID).filter(Ingredient_Name=ingredientName)
        ingredientPricePerGram = ingredient[0].Ingredient_PricePerGram
        totalIngredientPrice = ingredientPricePerGram * float(ingredientQuantity)
        recipe = RecipeRequirementsTable()
        recipe.Ingredient_Name = ingredientName
        recipe.Ingredient_Quantity = ingredientQuantity
        recipe.Ingredient_PricePerGram = ingredientPricePerGram
        recipe.Total_Ingredient_Price = totalIngredientPrice
        recipe.Ingredient_id = ingredient[0].id
        recipe.Item_id = ItemId
        recipe.Restaurant_id = Restaurant_ID
        recipe.save()
        menuItem=MenuItemsTable.objects.filter(id=ItemId)
        menuItem.update(Recipe=True)
        costPrice = 0
        recipeList = RecipeRequirementsTable.objects.filter(Restaurant_id=Restaurant_ID).filter(Item_id=ItemId)
        for item in recipeList:
            costPrice+=item.Total_Ingredient_Price
            ingredientList[item.Ingredient_Name] = item.Ingredient_Quantity
        menuItem.update(Cost_Price=round(costPrice,2))
        gst_margin = menuItem[0].Item_GST
        profit_margin = menuItem[0].Item_ProfitMargin
        gst = (gst_margin/100)*menuItem[0].Cost_Price
        profit = (profit_margin/100)*menuItem[0].Cost_Price
        sellingPrice = costPrice+gst+profit
        menuItem.update(Selling_Price=round(sellingPrice,2))
        return JsonResponse({'ingredientList':ingredientList})
    
    if request.method == 'GET':
        ingredientList = {}
        ItemId = request.GET['itemId']
        recipeList = RecipeRequirementsTable.objects.filter(Restaurant_id=Restaurant_ID).filter(Item_id=ItemId)
        ItemName = MenuItemsTable.objects.filter(Restaurant_id=Restaurant_ID).filter(id=ItemId)[0].Item_Name
        for item in recipeList:
            ingredientList[item.Ingredient_Name] = item.Ingredient_Quantity
        return JsonResponse({'ingredientList':ingredientList,'itemName':ItemName})
    
    ingredients = InventoryTable.objects.filter(Restaurant_id=Restaurant_ID)
    toPass = {'ingredients':ingredients,'recipeList':recipeList}
    return render(request, 'menuCustomization.html', toPass)

def manageCovers(request):
    manager = ManagerRegistrationTable.objects.filter(user_id=request.user.id)
    Restaurant_ID = manager[0].Restaurant_id
    if request.method=='POST':
        tableNumber = request.POST['tableNumber']
        covers = request.POST['covers']
        table = SeatManagementTable()
        table.Table_Number = tableNumber
        table.Number_Of_Covers = covers
        table.Restaurant_id = Restaurant_ID
        table.save()
        return redirect("manageCovers")
    else:
        seatDetails = SeatManagementTable.objects.filter(Restaurant_id = Restaurant_ID)
        restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
        toPass={'Restaurantdetails':restDetails, 'seatDetails':seatDetails}
        return render(request,"coverManagement.html", toPass)

def manageEmployees(request):
    admin = RestaurantRegistrationTable.objects.filter(user_id=request.user.id)
    Restaurant_ID = admin[0].user_id
    managerDetails = ManagerRegistrationTable.objects.filter(Restaurant_id = Restaurant_ID)
    staffDetails = StaffRegistrationTable.objects.filter(Restaurant_id = Restaurant_ID)
    managers = []
    staves = []

    if request.method == 'POST':
        employeeEmail = request.POST['employeeEmail']
        employeeSalary = request.POST['employeeSalary']
        employee = User.objects.filter(email = employeeEmail)
        if len(employee)<=0:
            messages.error(request,'Employee for given email does not exist!')
            return redirect('manageEmployees')
        else:
            employeeId = employee[0].id
            manager = managerDetails.filter(user_id = employeeId)
            staff = staffDetails.filter(user_id = employeeId)
            if len(manager) > 0:
                manager.update(Manager_Salary = employeeSalary)
            else :
                staff.update(Staff_Salary = employeeSalary)

    for manager in managerDetails:
        managerSalary = manager.Manager_Salary
        managerId = manager.user_id
        employeeDetails = User.objects.filter(id = managerId)[0]
        details={
            'name':(employeeDetails.first_name+" "+employeeDetails.last_name).title(),
            'email':employeeDetails.email,
            'contact':employeeDetails.contact,
            'address':employeeDetails.address,
            'salary':managerSalary,
            'joiningDate':str(employeeDetails.date_joined)[:10]
        }
        managers.append(details)

    for staff in staffDetails:
        staffSalary = staff.Staff_Salary
        staffDesignation = staff.Staff_designation
        staffId = staff.user_id
        employeeDetails = User.objects.filter(id = staffId)[0]
        details={
            'name':(employeeDetails.first_name+" "+employeeDetails.last_name).title(),
            'email':employeeDetails.email,
            'contact':employeeDetails.contact,
            'address':employeeDetails.address,
            'salary':staffSalary,
            'designation':staffDesignation,
            'joiningDate':str(employeeDetails.date_joined)[:10]
        }
        staves.append(details)

    restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
    toPass={'Restaurantdetails':restDetails, 'managers':managers, 'staves':staves}
    return render(request, "manageEmployees.html", toPass)

def salesRecords(request):
    manager = ManagerRegistrationTable.objects.filter(user_id=request.user.id)
    admin = RestaurantRegistrationTable.objects.filter(user_id=request.user.id)
    if len(manager) != 0 :
        Restaurant_ID = manager[0].Restaurant_id
    else:
        Restaurant_ID = admin[0].user_id
    completedOrders =  OrderManagementTable.objects.filter(Restaurant_id = Restaurant_ID).filter(Order_Completed = True)
    allCompletedOrders=[]
    for order in completedOrders:
        customerId = order.Customer_id
        customer = CustomerManagementTable.objects.filter(Restaurant_id = Restaurant_ID).filter(id = customerId)[0]
        currentOrder={
            'customerName':customer.Customer_Name,
            'customerContact':customer.Customer_Phone,
            'items':order.Items_Ordered[:-2],
            'type':order.Order_Type,
            'tableNumber':order.Table_Number,
            'discount':order.Discount_Percentage,
            'price':order.Amount_To_Pay,
            'date':order.Order_Date,
            'time':order.Order_Time,
            'invoice':order.Invoice
        }
        allCompletedOrders.append(currentOrder)
    restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
    toPass={'Restaurantdetails':restDetails, 'Completedorders':allCompletedOrders}
    if len(manager) != 0 :
        return render(request, "salesRecords.html", toPass)
    else:
        return render(request, "orderRecords.html", toPass)

def salesAnalysis(request):
    manager = ManagerRegistrationTable.objects.filter(user_id=request.user.id)
    admin = RestaurantRegistrationTable.objects.filter(user_id=request.user.id)
    if len(manager) != 0 :
        Restaurant_ID = manager[0].Restaurant_id
    else:
        Restaurant_ID = admin[0].user_id
    chart = 0
    if request.method=='POST':
        plotDate=request.POST['plotDate']
        orders=OrderManagementTable.objects.filter(Order_Date=plotDate)
        x=['midnight','1am','2am','3am','4am','5am','6am','7am','8am','9am','10am','11am',
            'noon','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm']
        y=[0]*24
        orderTime=[]
        for order in orders:
            orderTime.append(str(order.Order_Time)[:2])
        orderTime.sort()
        orderTime = [int(i) for i in orderTime]
        count=0
        for team in orderTime:
            count=orderTime.count(team)
            y[team] = count
        
        chart = getPlot(x,y,plotDate)
        if len(orders) == 0:
            chart=1

    restDetails = RestaurantRegistrationTable.objects.filter(user_id=Restaurant_ID)
    toPass={'Restaurantdetails':restDetails, 'chart':chart}
    if len(manager) != 0 :
        return render(request, "salesAnalysis.html", toPass)
    else:
        return render(request, "orderAnalysis.html", toPass)

def logout(request):
    auth.logout(request)
    return redirect('/')