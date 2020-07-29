let vm = new Vue({
    el: '.col-md-8',
    data: {
        newslists: [],
    },
    methods: {
        getnews: function () {
            $.get(
                'http://api.tianapi.com/areanews/index',
                {
                    'key': 'dfa319efc6ed6e4aa30f38804105bdfc',
                    'areaname': '湖北',
                    'num': '5'
                },
                function (data) {
                    for (let i=0;i<6;i++){
                        vm.newslists.push(data.newslist[i])
                    }
                    console.log(vm.newslists)
                }
            )
        }
    },
    mounted(){
        this.getnews();
    }
});
