$(function () {
    $('.glyphicon-heart-empty').click(function () {
        var post_id = $(this).attr('data-id');
        var status = $(this).prev().parent().attr('status');
        var url_target = '';
        url_target = '/front/dianzan/'
        $.get(
            url_target,
            {
                'post_id': post_id
            },
            function (data) {
                if (data['code'] === 200) {
                    window.location.reload()
                }
            }
        )

    })

    $('.glyphicon-heart').click(function () {
        var post_id = $(this).attr('data-id');
        var status = $(this).parent().attr('status');
        var url_target = '';
        url_target = '/front/cancel_dianzan/';
        $.get(
            url_target,
            {
                'post_id': post_id
            },
            function (data) {
                if (data['code'] === 200) {
                    window.location.reload()
                }
            }
        )

    })
})