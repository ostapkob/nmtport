 var app = new Vue({
    el: '#app',
    data: {
        counter: 3,
        text: 'This is the latest data for each mechanism',
        all_data: [],
        http : ['http://127.0.0.1:5000/api/v1.0/all_last_data', 'http://35.241.126.216/api/v1.0/all_last_data']
    },


        methods: {
            getData () {
                this.$http.get('/api/v1.0/all_last_data').then(response => {
                    this.all_data = response.body
                }, response => {
                    console.log('response err')
                });
            },
            // get_data() {
            //     axios.get(this.http[1]).then((response) => {
            //         this.all_data = response.data;
            //     });
            // },
        },
        created: function() {
            this.getData();
        },

        mounted: function() {
            this.$nextTick(function() {
                window.setInterval(() => {
                    this.getData();
                }, 5000);
            })
        },

    //    function() {this.getData();},

    filters: {
    DMtime: function(string) {
        return string.substring(5,12) + string.substring(17,22);
        }
  
  }




})

