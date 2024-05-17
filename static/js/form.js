// ajax    input   输入




$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault(); // 防止表单实际提交   Prevent the form from actually submitting

        var timeValue = $('#timeInput').val(); // 获取输入的时间值 Get the input time value

        // 无论timeValue的值如何，都发送Ajax请求到服务器  Send an Ajax request to the server regardless
        $.ajax({
            data: {
                time: timeValue
            },
            type: 'POST',
            url: '/process'
        })
        .done(function(data) {
			// 首先检查是否存在错误消息   check if there is an error message
			if (data.error) {
				// 如果存在错误消息，显示错误消息     there is an error
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			// 然后根据status字段判断是成功还是一般的错误消息   based on the status field
			else if (data.status === 'success') {
				// 如果服务器返回成功消息   returns a success
				$('#successAlert').text(data.message).show();
				$('#errorAlert').hide();
			} else if (data.status === 'error') {
				// 如果服务器返回一般的错误消息    returns a general error
				$('#errorAlert').text(data.message).show();
				$('#successAlert').hide();
			}
		});
		
    });
});


