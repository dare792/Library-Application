// toggle visivility when clicking on button
function showDropdown() {
    document.getElementById("menuDropdownContent").classList.toggle("show");
}

// Close sropdown when clicking outside of it
window.onclick = function(hideDropdown) {
    if (!hideDropdown.target.matches('.menuDropdown-btn'));
    var dropdowns = document.getElementsByClassName("menuDropdown-content");
    var i;
    for (i = 0; i < dropdowns.lenght; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
        }
    }
}