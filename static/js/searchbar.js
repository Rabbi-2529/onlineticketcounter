// const searchField = document.querySelector("#searchField");
// searchField.addEventListener("keyup", (e) => {
//   const searchValue = e.target.value;
//   if (searchValue.trim().length > 0) {
//     console.log("searchValue", searchValue);
//     fetch("/search_bus", {
//       body: JSON.stringify({ searchText: searchValue }),
//       method: "POST",
//     })
//       .then((res) => res.json())
//       .then((data) => {
//           console.log("data", data);
//           if (data.length == 0) {

//           }
//       });
//   }
// });

$(document).ready(function () {
  $("#bus-search-form").submit(function (event) {
    // Prevent the form from submitting in the default way
    event.preventDefault();

    // Get the form data
    var start_point = $("#start-point-input").val();
    var end_point = $("#end-point-input").val();
    var journey_date = $("#journey-date-input").val();

    // Send an AJAX request to the server
    $.ajax({
      url: "/search_bus/",
      type: "get",
      data: {
        start_point: start_point,
        end_point: end_point,
        journey_date: journeydate,
      },
      success: function () {
        // Redirect to the search results page
        window.location.href =
          "/results/?start_point=" +
          start_point +
          "&end_point=" +
          end_point +
          "journey_date" +
          journey_date;
      },
    });
  });
});
