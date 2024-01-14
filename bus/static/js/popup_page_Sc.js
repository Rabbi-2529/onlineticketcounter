const boardingLinks = document.querySelectorAll(".boarding-link");

boardingLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const boardingPoint = link.dataset.boarding;
    const modal = document.createElement("div");
    modal.classList.add("modal");
    const modalContent = document.createElement("div");
    modalContent.classList.add("modal-content");
    const closeBtn = document.createElement("span");
    closeBtn.classList.add("close");
    closeBtn.innerHTML = "&times;";
    modalContent.appendChild(closeBtn);
    const boardingHeader = document.createElement("h2");
    boardingHeader.innerHTML = "Boarding Point";
    modalContent.appendChild(boardingHeader);
    const boardingText = document.createElement("p");
    boardingText.innerHTML = boardingPoint;
    modalContent.appendChild(boardingText);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    modal.style.display = "block";
    closeBtn.addEventListener("click", () => {
      modal.style.display = "none";
      modal.remove();
    });
    window.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.style.display = "none";
        modal.remove();
      }
    });
  });
});
const droppingLinks = document.querySelectorAll(".dropping-link");

droppingLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const droppingPoint = link.dataset.dropping;
    const modal = document.createElement("div");
    modal.classList.add("modal");
    const modalContent = document.createElement("div");
    modalContent.classList.add("modal-content");
    const closeBtn = document.createElement("span");
    closeBtn.classList.add("close");
    closeBtn.innerHTML = "&times;";
    modalContent.appendChild(closeBtn);
    const droppingHeader = document.createElement("h2");
    droppingHeader.innerHTML = "Dropping Point";
    modalContent.appendChild(droppingHeader);
    const droppingText = document.createElement("p");
    droppingText.innerHTML = droppingPoint;
    modalContent.appendChild(droppingText);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    modal.style.display = "block";
    closeBtn.addEventListener("click", () => {
      modal.style.display = "none";
      modal.remove();
    });
    window.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.style.display = "none";
        modal.remove();
      }
    });
  });
});

const facilitiesLinks = document.querySelectorAll(".facilities-link");

facilitiesLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const facilities = link.dataset.facilities;
    if (facilities) {
      const modal = document.createElement("div");
      modal.classList.add("modal");
      const modalContent = document.createElement("div");
      modalContent.classList.add("modal-content");
      const closeBtn = document.createElement("span");
      closeBtn.classList.add("close");
      closeBtn.innerHTML = "&times;";
      modalContent.appendChild(closeBtn);
      const facilitiesHeader = document.createElement("h2");
      facilitiesHeader.innerHTML = "Facilities";
      modalContent.appendChild(facilitiesHeader);
      const facilitiesText = document.createElement("p");
      facilitiesText.innerHTML = facilities;
      modalContent.appendChild(facilitiesText);
      modal.appendChild(modalContent);
      document.body.appendChild(modal);
      modal.style.display = "block";
      closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
        modal.remove();
      });
      window.addEventListener("click", (e) => {
        if (e.target === modal) {
          modal.style.display = "none";
          modal.remove();
        }
      });
    } else {
      alert("No facilities available.");
    }
  });
});
