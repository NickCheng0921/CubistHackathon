document.addEventListener("DOMContentLoaded", function() {
    console.log("its bikin time");
});

document.addEventListener("DOMContentLoaded", function() {
	// Resize map
    var mapIframe = document.getElementById("map-iframe");
    mapIframe.style.width = (2*mapIframe.offsetWidth) + "px";

	// Resize contract list
	var screenHeight = window.innerHeight;
	document.getElementById("contract-list-container").style.height = screenHeight*0.75 + "px";


    // Find the list container
    var listContainer = document.getElementById("contract-list-container");

    // Loop to add 10 items
    for (var i = 1; i <= 100; i++) {
        // Create a new list item
        var newItem = document.createElement("li");
        newItem.textContent = "Item " + i;

        // Append the new item to the list container
        listContainer.appendChild(newItem);
    }
});
