$(function () {
    $('#capture_img').click(function () {
        // $.get(
        //     '/common',
        //     {},
        //     function (data) {
        //         $('#capture_img').attr('src','/common')
        //     }
        // )
        var self = $(this);
        var src = self.attr('src');
        self.attr('src','/common/capture'+"/?random="+Math.random());

    })
});