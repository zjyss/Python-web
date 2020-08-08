$(function () {
    $('#captcha-btn').click(function () {
        var email = $('#email').val();
        $.post(
            '/cms/email_capture',
            {'email':email},
            function (data) {
                if (data.code===200){
                    alert('验证码发送成功')
                }else {
                   alert('验证码发送失败')
                }
            }
        )
    });

    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var email = $('#email').val();
        var captcha = $('#captcha').val();
        $.post(
            '/cms/resetemail/',
            {
                'email':email,
                'captcha':captcha
            },
            function (data) {
                if (data.code===200){
                    alert('邮件修改成功');
                    $('#email').val('');
                    $('#captcha').val('')
                }else {
                    alert('邮件修改失败')
                }
            }
        )
    })
})