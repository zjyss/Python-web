$(function () {
    var ue = UE.getEditor('editor',{
        'serverUrl':'/uediter/upload/'
    });
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var title = $('input[name="title"]').val();
        var board_id = $('select[name="board_id"]').val();
        var content = ue.getContent();
        $.post(
            '/front/apost/',
            {
                'title':title,
                'board_id':board_id,
                'content':content
            },
            function (data) {
                if (data['code']===200){
                    xtalert.alertConfirm(
                        {
                            'msg':'发帖成功',
                            'cancelText':'回到首页',
                            'confirmText':'再发一篇',
                            'cancelCallback':function () {
                                //回到首页
                                window.location = '/'
                            },
                            'confirmCallback':function () {
                                $('input[name="title"]').val('');
                                ue.setContent('');
                                window.location.reload()
                            }
                        }
                    )
                }else {
                    xtalert.alertErrorToast('发布失败')
                }
            }
        )

    })
})