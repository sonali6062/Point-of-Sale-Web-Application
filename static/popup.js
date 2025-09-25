var popup = document.getElementById("popup");
var openPopup = document.getElementsByClassName("openPopup");
var closePopup = document.getElementById("closePopup");
var itemIdInput = document.getElementById("itemIdInput");
var addIngredientButton = document.getElementById("addIngredientButton");
var recipeButton = document.getElementsByClassName("recipeButton");
var recipeForm = document.getElementById("recipeForm");
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
var form = document.getElementById("recipeForm");

for(let item of openPopup){
	item.addEventListener("click", () => {
		itemIdInput.value = item.value;
		popup.style.display = "block";
		}
	)}

closePopup.addEventListener("click", () => {
		popup.style.display = "none";
	})

addIngredientButton.addEventListener("click", (e) => {
	e.preventDefault();
	let ingredientName = document.getElementById("ingredientName");
	let ingredientQuantity = document.getElementById("ingredientQuantity");
	var xhr = new XMLHttpRequest();
	xhr.open("POST","manageRecipe",true);
	xhr.onload=function(){
		if(xhr.status == 200){
			var obj = JSON.parse(xhr.responseText)
			var ingredientList = Object.values(obj)[0]
			addRecipeList(ingredientList)
		}		
	}
	xhr.setRequestHeader("X-CSRFToken", csrftoken);
	xhr.send(JSON.stringify({
		'itemId':itemIdInput.value,
		'ingredientName': ingredientName.value,
		'ingredientQuantity':ingredientQuantity.value
	}));
	form.reset();
})

for(btn of recipeButton){
	btn.addEventListener("click", (e)=>{
		e.preventDefault();
		var xhr=new XMLHttpRequest();
		xhr.open("GET",`manageRecipe?itemId=${itemIdInput.value}`,true)
		xhr.onload=function(){
			if(xhr.status == 200){
				var obj = JSON.parse(xhr.responseText)
				var ingredientList = Object.values(obj)[0]
				var itemName = Object.values(obj)[1]
				document.getElementById("popupItemName").innerHTML='Item Name: '+itemName;
				addRecipeList(ingredientList)
				console.log("yes1")
				}
			}
		xhr.send()
	})
}

function addRecipeList(ingredientList){
	let c=1
	let table = document.getElementById("recipeList")
	table.innerHTML = `<tr id="recipeListHeader">
						<th>S.no.</th>
						<th>Name</th>
						<th>Quantity</th>
						</tr>`
	for(let items in ingredientList){
		let row = document.createElement("tr")
		row.innerHTML = `<td>${c++}</td><td>${items}</td><td>${ingredientList[items]}grams</td>`
		row.class="ingredientList"
		table.appendChild(row)
}

}