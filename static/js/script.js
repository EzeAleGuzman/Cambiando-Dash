// Funcion para agregar evento click a elementos con ID
function submenu(subId) {
    var subBox = document.getElementById(subId);

    if (subBox.style.display === "none" || subBox.style.display === "") {
        subBox.style.display = "block";
    } else (subBox.style.display = "none");

}
