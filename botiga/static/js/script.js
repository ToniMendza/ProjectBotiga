document.addEventListener("DOMContentLoaded", function () {
    var dropdowns = document.querySelectorAll(".nav-item.dropdown");

    dropdowns.forEach(function (dropdown) {
        dropdown.addEventListener("mouseover", function () {
            var menu = this.querySelector(".dropdown-menu");
            if (menu) {
                menu.classList.add("show");
            }
        });

        dropdown.addEventListener("mouseleave", function () {
            var menu = this.querySelector(".dropdown-menu");
            if (menu) {
                menu.classList.remove("show");
            }
        });
    });
});