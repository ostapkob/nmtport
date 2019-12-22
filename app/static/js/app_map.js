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
                    paths: [
                        { lat: 42.817757, lng: 132.891146 },
                        { lat: 42.817139, lng: 132.893377 },
                    ] },
                {    paths: [
                        { lat: 42.814463, lng: 132.891906 },
                        { lat: 42.815187, lng: 132.889857},
                    ] },
                {      paths: [
                        { lat: 42.814636, lng: 132.888989 },
                        { lat: 42.814030, lng: 132.890888 },
                        { lat: 42.806978, lng: 132.886661 },
                        { lat: 42.807718, lng: 132.884998 }
                    ],
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 0.5,
                    fillColor: '#FF0000',
                    fillOpacity: 0.35
                }
            ],
        },
        methods: {
            get_data() {
                axios.get(this.http[0]).then((response) => {
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
