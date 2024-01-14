$(document).ready(function () {
  $("#id_email").keyup(function () {
    var email = $(this).val();

    if (email !== "") {
      $.ajax({
        url: "{% url 'check_email_exist' %}",
        type: "POST",
        data: { email: email },
      })
        .done(function (response) {
          console.log(response);
          if (response === "True") {
            $(".email_error").remove();
            $(
              "<span class='email_error' style='padding: 5px;color: red;font-weight: bold;'>Email Not Available</span>"
            ).insertAfter("#id_email");
            $("#id_email").addClass("error-field");
          } else {
            $(".email_error").remove();
            $(
              "<span class='email_error' style='padding: 5px;color: green;font-weight: bold;'>Email Available</span>"
            ).insertAfter("#id_email");
            $("#id_email").removeClass("error-field");
          }
        })
        .fail(function () {
          console.log("failed");
        });
    } else {
      $(".email_error").remove();
      $("#id_email").removeClass("error-field");
    }
  });

  $("#id_username").keyup(function () {
    var username = $(this).val();

    if (username !== "") {
      $.ajax({
        url: "{% url 'check_username_exist' %}",
        type: "POST",
        data: { username: username },
      })
        .done(function (response) {
          console.log(response);
          if (response === "True") {
            $(".username_error").remove();
            $(
              "<span class='username_error' style='padding: 5px;color: red;font-weight: bold;'>Username Not Available</span>"
            ).insertAfter("#id_username");
            $("#id_username").addClass("error-field");
          } else {
            $(".username_error").remove();
            $(
              "<span class='username_error' style='padding: 5px;color: green;font-weight: bold;'>Username Available</span>"
            ).insertAfter("#id_username");
            $("#id_username").removeClass("error-field");
          }
        })
        .fail(function () {
          console.log("failed");
        });
    } else {
      $(".username_error").remove();
      $("#id_username").removeClass("error-field");
    }
  });

  $("#phone_number").on("input", function () {
    var phoneNumber = $(this).val();
    var numericPhoneNumber = phoneNumber.replace(/\D/g, ""); // Remove non-digit characters

    $(this).val(numericPhoneNumber); // Update the input value with the numeric version

    // Check if the phone number length is not 11
    if (numericPhoneNumber.length !== 11) {
      $(".phone_error").remove();
      $(
        "<span class='phone_error' style='padding: 5px;color: red;font-weight: bold;'>Phone Number must be 11 digits</span>"
      ).insertAfter("#phone_number");
      $("#phone_number").addClass("error-field");
      return;
    }

    // Check if the phone number starts with the allowed prefixes
    var allowedPrefixes = ["019", "018", "017", "016", "013", "014"];
    var isValidPrefix = false;

    for (var i = 0; i < allowedPrefixes.length; i++) {
      if (numericPhoneNumber.startsWith(allowedPrefixes[i])) {
        isValidPrefix = true;
        break;
      }
    }

    if (!isValidPrefix) {
      $(".phone_error").remove();
      $(
        "<span class='phone_error' style='padding: 5px;color: red;font-weight: bold;'>Phone Number must start with 019, 018, 017, 016, 013, or 014</span>"
      ).insertAfter("#phone_number");
      $("#phone_number").addClass("error-field");
      return;
    }

    // Phone number is valid, proceed with availability check
    $(".phone_error").remove();
    $("#phone_number").removeClass("error-field");
    $.ajax({
      url: "{% url 'check_phone_number_exist' %}",
      type: "POST",
      data: { phoneNumber: numericPhoneNumber },
    })
      .done(function (response) {
        console.log(response);
        if (response === "True") {
          $(
            "<span class='phone_error' style='padding: 5px;color: red;font-weight: bold;'>Phone Number Not Available</span>"
          ).insertAfter("#phone_number");
          $("#phone_number").addClass("error-field");
        } else {
          $(
            "<span class='phone_error' style='padding: 5px;color: green;font-weight: bold;'>Phone Number Available</span>"
          ).insertAfter("#phone_number");
          $("#phone_number").removeClass("error-field");
        }
      })
      .fail(function () {
        console.log("failed");
      });
  });

  // Variables for delay and timeout
  var delayTimer;
  var timeout = 300;

  // Function to handle suggestion request
  function performSuggestion(query) {
    $.ajax({
      url: "/staff_suggestion_view/",
      type: "GET",
      data: {
        query: query,
      },
      success: function (response) {
        $("#suggestions").empty();
        $.each(response.suggestions, function (index, suggestion) {
          $("#suggestions").append("<p>" + suggestion + "</p>");
        });
      },
    });
  }

  // Function to handle search request
  function performSearch(query) {
    $.ajax({
      url: "/add_staff/",
      type: "GET",
      data: {
        query: query,
      },
      success: function (response) {
        $("#search-results").html(response);
      },
    });
  }

  // Event handler for search form submission
  $("#search-form").on("submit", function (event) {
    event.preventDefault();
    var query = $("#search-input").val();
    performSearch(query);
  });

  // Event handler for search input keyup
  $("#search-input").on("keyup", function (event) {
    var query = $(this).val();
    clearTimeout(delayTimer);
    if (query) {
      delayTimer = setTimeout(function () {
        performSuggestion(query);
      }, timeout);
    } else {
      $("#suggestions").empty();
    }
  });

  // Event handler for form submission
  $("form").on("submit", function (event) {
    var isValid = true;
    if ($("#id_email").hasClass("error-field")) {
      isValid = false;
    }
    if ($("#id_username").hasClass("error-field")) {
      isValid = false;
    }
    if ($("#phone_number").hasClass("error-field")) {
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault();
      $(".error-field").css("border-color", "red");
    }
  });
});
