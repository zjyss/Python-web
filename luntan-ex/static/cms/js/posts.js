$(function () {
    //删除帖子
    event.preventDefault();
    $('.btn-danger').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var post_id = self.val();
        $.post(
            '/cms/delete_post/',
            {
                'post_id': post_id
            },
            function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast('移除成功');
                    self.parent().parent().remove()
                } else {
                    xtalert.alertErrorToast('移除失败')
                }
            }
        )
    });

    $('.btn-default').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var post_id = self.next().val();
        var status = self.parent().parent().attr('data-highlight');
        var target_url = '';
        if (status==='1'){
            target_url = '/cms/un_good_post/'
        }else {
            target_url = '/cms/good_post/'
        }
        $.get(
            target_url,
            {
                'post_id': post_id
            },
            function (data) {
                if (data['code']===200) {
                    if (status==='1'){
                        xtalert.alertSuccessToast('取消加精成功');
                        window.location.reload()
                    }else {
                        xtalert.alertSuccessToast('加精成功')
                        window.location.reload()
                    }
                } else {
                    if (status==='1'){
                        xtalert.alertSuccessToast('取消加精失败');
                    }else {
                        xtalert.alertSuccessToast('加精失败')
                    }
                }
            }
        )
    })
});