$(function () {
    $('#add-board-btn').click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            "text":"添加板块",
            "placeholder":"请输入板块名称",
            "confirmCallback":function (inputValue) {
                // alert('输入了'+inputValue);
                $.post(
                    '/cms/addboard/',
                    {
                        'name':inputValue
                    },
                    function (data) {
                        if (data['code']===200){
                            xtalert.alertSuccessToast('添加成功');
                            window.location.reload()
                        }else {
                            xtalert.alertErrorToast('添加失败')
                        }
                    }
                )
            }
        })
    });
    $('.delete-board-btn').click(function () {
        var self = $(this)
        var id = $(this).parent().parent().attr('data-id');
        $.post(
            '/cms/delete_board/',
            {
                'id':id
            },
            function (data) {
                if (data['code']===200){
                    xtalert.alertSuccessToast('删除成功')
                    // self.parent().parent().display('none');
                    self.parent().parent().remove();
                }else {
                    xtalert.alertSuccessToast('删除失败')
                }
            }
        )
    });
    $('.edit-board-btn').click(function () {
        var self = $(this);
        var id = $(this).parent().parent().attr('data-id');
        var board_name = self.parent().prev().prev().prev().html();
        xtalert.alertOneInput({
            "text":"修改板块名称",
            "placeholder":board_name,
            'confirmCallback':function (inputValue) {
                $.post(
                    '/cms/edit_board/',
                    {
                        'id':id,
                        'name':inputValue
                    },
                    function (data) {
                        if (data['code']===200){
                            xtalert.alertSuccessToast('修改成功');
                            self.parent().prev().prev().prev().html(inputValue)
                        }else {
                            xtalert.alertSuccessToast('修改失败')
                        }
                    }
                )
            }
        })
    })
})