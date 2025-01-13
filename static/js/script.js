// Funcion para agregar evento click a elementos con ID
function submenu(subId) {
    var subBox = document.getElementById(subId);

    if (subBox.style.display === "none" || subBox.style.display === "") {
        subBox.style.display = "block";
    } else (subBox.style.display = "none");

}

function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    var navbarCollapse = document.querySelector('.navbar-collapse');
    sidebar.classList.toggle('collapsed');
    navbarCollapse.classList.remove('show');
}

function toggleNavbar() {
    var sidebar = document.querySelector('.sidebar');
    var navbarCollapse = document.querySelector('.navbar-collapse');
    navbarCollapse.classList.toggle('show');
    sidebar.classList.add('collapsed');
}