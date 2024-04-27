document.addEventListener("DOMContentLoaded", function() {
    console.log("its bikin time");
});

document.addEventListener("DOMContentLoaded", function() {
	// Resize contract list
	var screenHeight = window.innerHeight;
	document.getElementById("contract-list-container").style.height = screenHeight*0.8 + "px";

    // Loop to add 10 items
    let table = document.getElementById("contract-table").getElementsByTagName('tbody')[0];
    for (var i = 1; i <= 10; i++) {
        var newRow = table.insertRow();
        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        var cell4 = newRow.insertCell(3)
        cell1.innerHTML = "Station " + i;
        cell2.innerHTML = i;
        cell3.innerHTML = i;
        cell4.innerHTML = "00:00:00";
    }
});
