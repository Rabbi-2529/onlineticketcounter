// $(document).ready(function() {
//     // Show the popup when a district is clicked
//     $('.district').click(function() {
//       // Get the district ID from the data attribute
//       var districtId = $(this).data('district-id');
  
//       // Set the heading of the popup
//       $('#popup-heading').text($(this).text() + ' Counters');
  
//       // Show the popup
//       $('#popup').modal('show');
  
//       // Load the counters for the clicked district via AJAX
//       $.ajax({
//         url: '/district/' + districtId + '/counters/',
//         success: function(data) {
//           // Update the contents of the popup with the loaded data
//           $('#popup-content').html(data);
//         },
//         error: function() {
//           // Show an error message if the AJAX request fails
//           $('#popup-content').html('<p>Sorry, something went wrong.</p>');
//         }
//       });
//     });
  
//     // Hide the popup when the close button is clicked
//     $('#popup-close').click(function() {
//       $('#popup').modal('hide');
//     });
//   });
  