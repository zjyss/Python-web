// function Restpasswd() {
//
// }
//
// Restpasswd.prototype.ListenSubmit=function () {
//     $('#submit').click(function (event) {
//         alert(111);
//         event.preventDefault();
//         var oldpassword = $('#oldpassword').val();
//         var newpassword = $('#newpassword').val();
//         var newpassword2 = $('#newpassword2').val();
//         alert(oldpassword);
//         jingyuajax.post({
//             'url':'/cms/resetpassword/',
//             'data':{'oldpassword': oldpassword,
//              'newpassword': newpassword,
//              'newpassword2': newpassword2,
//             },
//             'success':function (data) {
//                 alert(111)
//             }
//         })
//
//     })
// };
//
// Restpasswd.prototype.run=function () {
//     var self = this;
//     self.ListenSubmit()
// };
//
// //实例化，调用run
// $(function () {
//     alert(111)
//     var setpass = Restpasswd();
//     setpass.run()
// });
$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var oldpassword = $('#oldpassword').val();
        var newpassword = $('#newpassword').val();
        var newpassword2 = $('#newpassword2').val();
        $.post(
            '/cms/resetpassword/',
            {
                'oldpassword':oldpassword,
                'newpassword':newpassword,
                'newpassword2':newpassword2,
            },
            function (data) {
                alert(data.message);

            }
        )
    })
})