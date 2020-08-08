let vm = new Vue({
    el: '.col-md-8',
    data: {
        newslists: [],
    },
    methods: {
        getnews: function () {

            $.get(
                '',
                {
                    
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
