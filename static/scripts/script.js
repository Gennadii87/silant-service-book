function openModal() {
    var modalContainer = document.getElementById("myModalContainer");
    modalContainer.style.display = "block";
    setTimeout(closeModal, 8200);
}
function closeModal() {
    var modalContainer = document.getElementById("myModalContainer");
    modalContainer.style.display = "none";
    setTimeout(openModal, 10000);
}
