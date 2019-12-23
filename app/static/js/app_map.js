Vue.use(VueGoogleMaps, {
    load: {
        key: 'AIzaSyDEEA8HUpeyr66BT6arigNEcKgqckkSDUg',
        v: 'quarterly',
    },
    installComponents: false,
});
document.addEventListener('DOMContentLoaded', function() {
    Vue.component('google-map', VueGoogleMaps.Map);
    Vue.component('google-marker', VueGoogleMaps.Marker);
    Vue.component('google-poligon', VueGoogleMaps.Polygon);
    Vue.component('google-info', VueGoogleMaps.InfoWindow);
    Vue.component('ground-overlay', VueGoogleMaps.MapElementFactory({
        mappedProps: {
            'opacity': {}
        }

        ,
        props: {
            'source': { type: String },
            'bounds': { type: Object },
        },
        events: ['click', 'dblclick'],
        name: 'groundOverlay',
        ctr: () => google.maps.GroundOverlay,
        ctrArgs: (options, { source, bounds }) => [source, bounds, options],
    }));
    new Vue({
        el: '#root',
        data: {
            place: '',
            all_data: [],
            http: ['http://127.0.0.1:5000/api/v1.0/all_last_data_ico', 'http://35.241.126.216/api/v1.0/all_last_data_ico'],
            markers: [
                { position: { lat: 42.8150, lng: 132.8907 }, title: 'Screen5', icon: 'http://maps.google.com/mapfiles/kml/pal3/icon12.png' }
            ],

            poligons: [{
                    paths: [ //7
                        { lat: 42.817757, lng: 132.891146 },
                        { lat: 42.817139, lng: 132.893377 },
                    ] ,
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 0.5,
                    fillColor: '#FF0000',
                    fillOpacity: 0.35
                },

                {paths: [ //9
                        { lat: 42.814463, lng: 132.891906 },
                        { lat: 42.815187, lng: 132.889857 },
                    ] },

                {paths: [ //10
                        { lat: 42.812937, lng: 132.890043 },
                        { lat: 42.813219, lng: 132.889027 },
                    ] },

                {paths: [//11
                        { lat: 42.811768, lng: 132.889450 },
                        { lat: 42.812154, lng: 132.888277 },
                    ] },

                {paths: [//12
                        { lat: 42.810566, lng: 132.888813 },
                        { lat: 42.810933, lng: 132.887553 },

                    ] },

                {paths: [ //13
                        { lat: 42.809348, lng: 132.888050 },
                        { lat: 42.809736, lng: 132.886782 },

                    ] },
                {paths: [//14
                        { lat: 42.808023, lng: 132.887264 },
                        { lat: 42.808419, lng: 132.886047 },
                    ] },

            ],
        },
        methods: {
            get_data() {
                axios.get(this.http[1]).then((response) => {
                    this.all_data = response.data;
                });
            },
        },
        created: function() {
            this.get_data();
        },

        mounted: function() {
            this.$nextTick(function() {
                window.setInterval(() => {
                    this.get_data();
                }, 5000);
            })
        },



    });
});
