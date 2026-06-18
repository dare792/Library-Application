// toggle visivility when clicking on button
function showDropdown() {
    document.getElementById("menuDropdownContent").classList.toggle("show")
    document.getElementById("menuDropdownContent").classList.toggle("flat-top-right")

    document.getElementById("menuDropdownContent").animate(
        [ {opacity: 0, transform: "translateY(-10px)"}, {opacity: 1, transform: "translateY(0)"}],
        {duration: 300, easing: "ease"}
    )

    document.getElementById("visual-dropdown-flat").classList.toggle("flat-left")
    document.getElementById("button-dropdown-flat").classList.toggle("flat-left")
}

// Close sropdown when clicking outside of it
window.onclick = function(hideDropdown) {
    if (!hideDropdown.target.matches('.menuDropdown-btn')) {
    var dropdowns = document.getElementsByClassName("menuDropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show')
            openDropdown.classList.remove('flat-top-right');
        }
    }
    if (document.getElementById("visual-dropdown-flat").classList.contains('flat-left'))
        document.getElementById("visual-dropdown-flat").classList.remove('flat-left');

    if (document.getElementById("button-dropdown-flat").classList.contains('flat-left'))
        document.getElementById("button-dropdown-flat").classList.remove('flat-left');
    }
}