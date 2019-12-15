


<template>
    <div class="container">
        <google-map :name="name"></google-map>
		<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDEEA8HUpeyr66BT6arigNEcKgqckkSDUg"></script>
    </div>
</template>

<script>
    import googleMap from '~/components/googleMap.vue'
    export default {
        data: function () {
            return {
                name: 'map'
            }
        },
        mounted: function () {
        },
        components: {googleMap}
    }
</script>

