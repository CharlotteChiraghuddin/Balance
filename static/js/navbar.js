const toggleBtn = document.querySelector(".toggle_btn");
const toggleBtnIcon = document.querySelector(".more img");
const dropdownMenu = document.querySelector(".dropdown_menu");

toggleBtn.onclick = function () {
    dropdownMenu.classList.toggle("open");

    const isOpen = dropdownMenu.classList.contains("open");

    toggleBtnIcon.src = isOpen
        ? "../static/assets/images/close.png"
        : "../static/assets/images/menu.png";
};