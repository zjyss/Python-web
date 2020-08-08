$(function () {
    $('#btn-submit').click(function (event) {
        event.preventDefault()
        var search_tips = $('.form-control').val()
        window.location.href='/front/search/?search_tips='+search_tips
        // window.location.href='/front/login/'
        //  $(window).attr('location','/front/login/');
        // $.get(
        //     '/front/search/',
        //     {
        //         'search_tips':search_tips
        //     },
        //     function (data) {
        //         window.location.href='/front/search/?search_tips='+search_tips
        //     }
        // )
    })
})