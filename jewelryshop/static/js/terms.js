var tabLists = document.querySelectorAll(".tabs_list ul li");
var tabItems = document.querySelectorAll(".tab_item");

tabLists.forEach(function(list) {
    list.addEventListener("click", function() {
        var tabData = list.getAttribute("data-tc");

        // Remove active class from all tabs
        tabLists.forEach(function(list) {
            list.classList.remove("active");
        });

        // Add active class to the clicked tab
        list.classList.add("active");

        // Hide all tab content items
        tabItems.forEach(function(item) {
            item.style.display = "none";
        });

        // Show the clicked tab content
        document.querySelector("." + tabData).style.display = "block";
    });
});

// Set the default active tab content on page load
document.querySelector(".tab_item_1").style.display = "block";
