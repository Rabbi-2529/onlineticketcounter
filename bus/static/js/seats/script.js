var firstSeatLabel = 1;
var booked = localStorage.getItem("booked")
  ? JSON.parse(localStorage.getItem("booked"))
  : [];
var coachNumber = getCoachNumberFromURL(); // Get coach number from URL
var price = getPriceFromURL(); // Get price from URL

$(document).ready(function () {
  var currentURL = window.location.href;
  var newURL = currentURL.split("?")[0];
  history.replaceState(null, null, newURL);
  var $cart = $("#selected-seats"),
    $counter = $("#counter"),
    $total = $("#total"),
    sc;

  function initializeSeatCharts(coachNumber, price) {
    var map = getSeatMap(coachNumber);

    sc = $("#bus-seat-map").seatCharts({
      map: map,
      seats: {
        f: {
          price: parseFloat(price) || 0, // Use the retrieved price, default to 0 if NaN
          classes: "first-class",
          category: "First Class",
        },
        e: {
          price: parseFloat(price) || 0, // Use the retrieved price, default to 0 if NaN
          classes: "economy-class",
          category: "Economy Class",
        },
      },
      naming: {
        top: false,
        getLabel: function (character, row, column) {
          return firstSeatLabel++;
        },
      },
      legend: {
        node: $("#legend"),
        items: [
          ["f", "available", "First Class"],
          ["e", "available", "Economy Class"],
          ["f", "unavailable", "Already Booked"],
        ],
      },
      click: function () {
        if (this.status() == "available") {
          $(
            "<li>" +
              this.data().category +
              " Seat #" +
              this.settings.label +
              ": <b>$" +
              this.data().price +
              '</b> <a href="#" class="cancel-cart-item">[cancel]</a></li>'
          )
            .attr("id", "cart-item-" + this.settings.id)
            .data("seatId", this.settings.id)
            .appendTo($cart);

          $counter.text(sc.find("selected").length + 1);
          $total.text(recalculateTotal(sc) + this.data().price);

          return "selected";
        } else if (this.status() == "selected") {
          $counter.text(sc.find("selected").length - 1);
          $total.text(recalculateTotal(sc) - this.data().price);

          $("#cart-item-" + this.settings.id).remove();

          return "available";
        } else if (this.status() == "unavailable") {
          return "unavailable";
        } else {
          return this.style();
        }
      },
    });

    // Set seat icons
    sc.find("f.available")
      .status("available")
      .seat.addClass("icon-first-class")
      .on("click", function () {
        // Handle click event for first class seats
        var seatId = $(this).attr("id");
        // Custom logic for handling click on first class seats
        // Example: Open a modal, display seat information, etc.
        console.log("Clicked on First Class seat: " + seatId);
      });

    sc.find("e.available")
      .status("available")
      .seat.addClass("icon-economy-class")
      .on("click", function () {
        // Handle click event for economy class seats
        var seatId = $(this).attr("id");
        // Custom logic for handling click on economy class seats
        // Example: Open a modal, display seat information, etc.
        console.log("Clicked on Economy Class seat: " + seatId);
      });

    booked.forEach(function (seat) {
      sc.get(seat).status("unavailable");
    });
  }

  function getSeatMap(coachNumber) {
    var seatMaps = {
      1010: ["ff_ff", "ff_ff", "ee_ee", "ee_ee", "ee_ee", "ee_ee", "ee_ee"],
      1011: [
        "ff_ff",
        "ff_ff",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
      ],
      1012: [
        "ff_ff",
        "ff_ff",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "eeeee",
      ],
      1013: [
        "ff_ff",
        "ff_ff",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
      ],
      1014: [
        "ff_ff",
        "ff_ff",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "eeeee",
      ],
      1015: [
        "ff_ff",
        "ff_ff",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
      ],
      1016: [
        "ff_ff",
        "ff_ff",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "ee_ee",
        "eeeee",
      ],

      // Add more seat maps for other coach numbers if needed
    };

    return seatMaps[coachNumber];
  }

  function recalculateTotal(sc) {
    var total = 0;
    sc.find("selected").each(function () {
      total += parseFloat(this.data().price);
    });
    return total;
  }

  initializeSeatCharts(coachNumber, price);
});

function getCoachNumberFromURL() {
  var urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("coachnumber");
}

function getPriceFromURL() {
  var urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("price");
}

$(function () {
  $("#checkout-button").click(function () {
    var items = $("#selected-seats li");
    if (items.length <= 0) {
      alert("Please select at least 1 seat first.");
      return false;
    }
    var selected = [];
    items.each(function (index, element) {
      var id = $(element).attr("id");
      id = id.replace("cart-item-", "");
      selected.push(id);
    });
    if (booked.length > 0) {
      selected = selected.concat(booked);
    }
    localStorage.setItem("booked", JSON.stringify(selected));
    alert("Seats have been reserved successfully.");
    location.reload();
  });

  $("#reset-btn").click(function () {
    if (confirm("Are you sure you want to reset the seat reservation?")) {
      localStorage.removeItem("booked");
      alert("Seats have been reset successfully.");
      location.reload();
    }
  });
});
