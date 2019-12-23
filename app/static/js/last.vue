 var app = new Vue({
    el: '#app',
    data: {
        counter: 3,
        text: 'This is the latest data for each mechanism',
        all_data: [],
        http : ['http://127.0.0.1:5000/api/v1.0/all_last_data', 'http://35.241.126.216/api/v1.0/all_last_data']
    },
    methods: {
        get_data() {
            axios.get(this.http[0]).then((response) => {
                this.all_data=response.data;
            });
        },
        parse(n) {
            return n;
        }

    },
    mounted: function () {
        this.$nextTick(function () {
            window.setInterval(() => {
                this.get_data();
            },5000);
        })
    },

    created: function () {
        this.get_data();
    },

    filters: {
  
    DMtime: function(string) {
        return string.substring(5,12) + string.substring(17,22);
        }
  
  }




})

