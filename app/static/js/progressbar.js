 var app = new Vue({
    el: '#app',
    data: {
        timestamp: "",
        counter: 4,
        test: true,
        all_data: [],
        http : jshttp,
        api : '',
        shift: '',
        date_shift: '',
        hs:[],
    },
    methods: {
        hight() {
            this.counter++;
            console.log(this.status);
        },
        getData() {
            axios.get(this.api).then((response) => {
                console.log(response.data);
                this.all_data=response.data;
            });
        },
        getNow: function() {
            let hour;
            const today = new Date();
            hour=today.getHours();
            if (hour>=8 && hour<20) {
                this.date_shift= today.getDate()+'.'+(today.getMonth()+1)+'.'+today.getFullYear();
                this.shift=1;
            }
            else if (hour<8) {
                this.date_shift= (today.getDate()-1)+'.'+(today.getMonth()+1)+'.'+today.getFullYear();
                this.shift=2;
            }
            else {
                this.date_shift= today.getDate()+'.'+(today.getMonth()+1)+'.'+today.getFullYear();
                this.shift=2
            }
            this.api='http://127.0.0.1:5000/api/v1.0/get_data/usm/'+this.date_shift+'/'+this.shift
            if (this.shift==1) {
                this.hs = ["║",  "╵", "09",  "╵", "10",  "╵", "11",  "╵", "12",  "╵", "13",  "╵", "14",  "╵", "15",  "╵", "16",  "╵", "17",  "╵", "18",  "╵", "19",  "╵",  "║"] }
                else {
                    this.hs = ["║",  "╵", "21",  "╵", "22",  "╵", "23",  "╵", "00",  "╵", "01",  "╵", "02",  "╵", "03",  "╵", "04",  "╵", "05",  "╵", "06",  "╵", "07",  "╵",  "║"] }
                },
            },
    mounted: function () {
        this.$nextTick(function () {
            window.setInterval(() => {
                this.getNow();
                this.getData();
            },10000);
        })
    },

    created: function () {
        this.getNow();
        this.getData();
    },
})

