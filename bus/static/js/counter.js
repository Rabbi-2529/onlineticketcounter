var popup = document.getElementsByClassName("popup")[0];
var closeBtn = document.getElementsByClassName("close")[0];

function openPopup() {
  popup.style.display = "block";
}

function closePopup() {
  popup.style.display = "none";
}

closeBtn.onclick = function () {
  closePopup();
};

window.onclick = function (event) {
  if (event.target == popup) {
    closePopup();
  }
};
$(document).ready(function () {
  // Show modal on page load
  $("#myModal").modal("show");

  // Handle OK button click
  $("#modal-ok-button").click(function () {
    window.location.href = "index.html";
  });
});
