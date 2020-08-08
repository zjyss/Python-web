$(function () {
    var ue = UE.getEditor('editor',{
        'serverUrl':'/uediter/upload/',
        'toolbars':[
            [
                'undo',
                'redo',
                'bold',
                'bold',
                'italic',
                'underline',
                'source',
                'blockquote',
                'selectall',
                'fontfamily',
                'fontsize',
                'simpleupload',
                'emotion',
            ]
        ]
    });
    window.ue = ue
});

$(function () {
    $('#comment-btn').click(function (event) {
        event.preventDefault();
        var content = window.ue.getContent()
        var post_id = $('#post-content').attr('data-id')
        $.get(
            '/front/common/',
            {
                'post_id':post_id,
                'content':content
            },
            function (data) {
                if (data['code']===200){
                    xtalert.alertSuccessToast('评论成功')
                    window.location.reload()
                }else {
                    xtalert.alertErrorToast('评论失败')
                }
            }
        )
    })
});