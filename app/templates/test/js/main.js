new Vue({
    el: '#app',
    data: {
        name: 'Hellow',
        styleCSS: '',
        value:1,
        show: false
            },

    methods: {
        ChangeText() {
            this.name = "Any Text"
            this.lable = "Yuo"
        }
    ,
    increment (value) {
        this.value = value
        if (value == 123)
            alert ('123')
    }
},
    computed: {
        doublevalue () {
            return this.value*2
        }
    }
})

