var order = document.getElementById("orderButton");
var popup = document.getElementById("orderPopup");
var form = document.getElementById("orderPopupForm");
var close = document.getElementById("closePopup");
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
var date = new Date()
var CustomerName
var CustomerPhone
var CustomerId
    
close.addEventListener("click", ()=>{
    if (CustomerId == null){
        popup.style.display="none";
        return
    }
    let xhr = new XMLHttpRequest()
    xhr.open("GET",`deleteOrder?customerId=${CustomerId}`,true)
    xhr.send()
    popup.style.display="none";
    })

order.addEventListener("click", selectCustomer);

function selectCustomer(){
    form.innerHTML=`
        <input id="customerName" class='orderField' type='text' name='customerName' placeholder='Enter customer name' required="true">
        <input id="customerPhone" class='orderField' type='number' name='customerPhone' placeholder='Enter customer contact' required="true">
        <input id='goToItemSelection' class='nextButton' type='button' value='>'>
    `
    popup.style.display="flex";
    popup.style.justifyContent="center";
    popup.style.alignItems="center";
    document.getElementById('goToItemSelection').addEventListener("click",selectItems);

}

function selectItems(){
    CustomerName = document.getElementById("customerName").value
    CustomerPhone = document.getElementById("customerPhone").value
    let xhr = new XMLHttpRequest();
	xhr.open("POST","manageCustomers",true);
	xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onload=function(){
		if(xhr.status == 200){
			var obj = JSON.parse(xhr.responseText)
            CustomerId = obj['customerId']
		}		
	}
	xhr.send(JSON.stringify({
		'customerName':CustomerName,
		'customerPhone':CustomerPhone,
	}));

    form.innerHTML =`
        <input id="itemName" class='orderField' type='text' name='itemName' placeholder='Enter item name' required="true">
        <input id="itemQuantity" class='orderField' type='number' name='itemQuantity' placeholder='Enter item quantity' required="true">
        <input id="itemDiscount" class='orderField' type='number' name='itemDiscount' placeholder='Enter item discount'>
        <button id='addItemButton' type='button'>Add Item to Order</button>
        <input id='goToFireKOT' class='nextButton' type='button' value='>'>
    `
    document.getElementById('goToFireKOT').addEventListener("click",fireKOT);
    document.getElementById('addItemButton').addEventListener("click",addToOrder);
}

function fireKOT(){
    form.innerHTML =`
        <div id="KOTDiv">
            <div id="KOTDivForm">
                <p>Customer Name: <b>${CustomerName}</b></p>
                <p>Customer Contact: <b>${CustomerPhone}</b></p>
                <p>Order Date: <b>${date.getDate()}/${date.getMonth()}/${date.getFullYear()}</b></p><br>
                <input id="orderType" list="orderTypeList" class='orderField' type='text' name='orderType' placeholder='Enter type of order' required="true">
                <datalist id="orderTypeList">
                    <option value="Dine-in">Dine-in</option>
                    <option value="Takeaway">Takeaway</option>
                    <option value="Delivery">Delivery</option>
                </datalist>
                <input id="seatsRequired" class='orderField' type='number' name='seatsRequired' placeholder='Enter seats required'>
                <input id="tableNumber" class='orderField' type='number' name='tableNumber' placeholder='Enter table number'>
                <input id="orderDiscount" class='orderField' type='number' name='orderDiscount' placeholder='Enter discount amount'>
            </div>
            <div id="KOTDivTable">
                <div id="tableDiv">
                    <table id="orderDetailTable">
                        <tr id="orderDetailTableHeader">
                            <th>S.No.</th>
                            <th>Item Name</th>
                            <th>Qty.</th>
                            <th>Price</th>
                        </tr>
                    </table>
                </div>
                <div id="amountDiv">
                    <label for='totalPrice'>Total Price:</label>
                    <input id="totalPrice" class="amountDivField" type='text' name='totalPrice'></input><br><br>
                    <label for='amountRecieved'>Amount Recieved:</label>
                    <input id="amountRecieved" class="amountDivField" type='text' name='amountRecieved' required="true"></input><br><br>
                    <label for='returnBalance'>returnBalance to return:</label>
                    <input id="returnBalance" class="amountDivField" type='text' name='returnBalance'></input><br><br>
                </div>
                <div id="KOTDivButtons">
                    <input id='fireKOTButton' type='button' value='Fire KOT'>
                    <input id='cancelOrderButton' type='submit' value='Cancel Order'>
                </div>
            </div>
        </div>
    `
    let xhr = new XMLHttpRequest()
    xhr.open('GET',`getOrder?customerId=${CustomerId}`,true)
    xhr.onload=function(){
        if(xhr.status == 200){
            let obj = Object.values(JSON.parse(xhr.responseText))[0]
            let count=1, totalItemCost = 0
            for (items in obj){
                let itemName = obj[items][0]
                let itemQty = obj[items][1]
                let itemCost = obj[items][2]
                let row = document.createElement("tr")
                row.innerHTML = `<td>${count}</td>
                                 <td>${itemName}</td>
                                 <td>${itemQty}</td>
                                 <td>${itemCost}</td>`
                document.getElementById("orderDetailTable").appendChild(row)
                totalItemCost += itemCost
                count++
            document.getElementById("totalPrice").value = totalItemCost
            price = totalItemCost
            }
        }
    }
    xhr.send()
    
    let totalPrice = document.getElementById("totalPrice")
    totalPrice.disabled = true
    let amountRecieved = document.getElementById("amountRecieved")
    let returnBalance = document.getElementById("returnBalance")
    returnBalance.disabled = true
    var cost

    
    function setreturnBalance(){
        returnBalance.value = (amountRecieved.value - totalPrice.value).toFixed(2)
        if(amountRecieved.value == ""){
            returnBalance.value=""
        }
        if(amountRecieved.value == "f" || amountRecieved.value == "full" || amountRecieved.value == "Full"){
            returnBalance.value="0.00"
        }
    }

    amountRecieved.onkeyup = setreturnBalance;

    let orderDiscount = document.getElementById("orderDiscount")
    orderDiscount.addEventListener("focus",setPrice,{once:true})
    function setPrice(){
        cost = totalPrice.value
    }
    orderDiscount.onkeyup=()=>{
        discount = (orderDiscount.value/100)*cost
        totalPrice.value = (cost - discount).toFixed(2)
        setreturnBalance()
    }

    var orderType = document.getElementById("orderType")
    var seatsRequired = document.getElementById("seatsRequired")
    var tableNumber = document.getElementById("tableNumber")
    orderType.onkeyup=()=>{
        if(orderType.value == "Delivery" || orderType.value == "Takeaway"){
            seatsRequired.disabled=true
            tableNumber.disabled=true
        }
        else{
            seatsRequired.disabled=false
            tableNumber.disabled=false
        }
    }

    document.getElementById("fireKOTButton").addEventListener("click",addKOT)
    document.getElementById("cancelOrderButton").addEventListener("click",cancelOrder)
}

function addToOrder(){
    var itemName = document.getElementById('itemName').value
    var itemQuantity = document.getElementById('itemQuantity').value
    var itemDiscount = document.getElementById('itemDiscount').value
    let xhr = new XMLHttpRequest()
    xhr.open("POST","takeOrder",true)
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(JSON.stringify({
        'itemName':itemName,
        'itemQuantity':itemQuantity,
        'itemDiscount':itemDiscount,
        'customerId': CustomerId
    }))
    form.reset()
}

function addKOT(){
    if(orderType.value == "Takeaway" || orderType.value == "Delivery"){
        seatsRequired.value = null
        tableNumber.value = null
    }

    let xhr = new XMLHttpRequest()
    xhr.open("POST","manageKOTS",true)
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onload=function(){
        window.location.replace('manageKOTS')
    }
    xhr.send(JSON.stringify({
        'customerId': CustomerId,
        'orderType':orderType.value,
        'seatsRequired':seatsRequired.value,
        'tableNumber':tableNumber.value,
        'orderDiscount':orderDiscount.value,
        'totalPrice':totalPrice.value,
        'amountRecieved':amountRecieved.value,
        'returnBalance':returnBalance.value,
    }))
}

function cancelOrder(){
    let xhr = new XMLHttpRequest()
    xhr.open("GET",`deleteOrder?customerId=${CustomerId}`,true)
    xhr.onload=function(){
        if(xhr.status == 200){
            window.location.reload()
        }
    }
    xhr.send()
}
