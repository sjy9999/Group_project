// ajax    input   

$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault(); //   Prevent the form from actually submitting

        var timeValue = $('#timeInput').val(); // Get the input time value

        // Send an Ajax request to the server regardless
        $.ajax({
            data: {
                time: timeValue
            },
            type: 'POST',
            url: '/process'
        })
        .done(function(data) {
			//    check if there is an error message
			if (data.error) {
				// there is an error
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			//  based on the status field
			else if (data.status === 'success') {
				//  returns a success
				$('#successAlert').text(data.message).show();
				$('#errorAlert').hide();
			} else if (data.status === 'error') {
				//  returns a general error
				$('#errorAlert').text(data.message).show();
				$('#successAlert').hide();
			}
		});
		
    });
});


