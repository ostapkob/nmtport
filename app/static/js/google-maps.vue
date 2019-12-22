<template>
  <div>
    <GmapMap :center="center" :map-type-id="mapTypeId" :zoom="15">
      <GmapMarker
        v-for="(item, index) in markers"
        :key="index"
        :position="item.position"
        :title="item.title"
        :icon="item.icon"
        @click="center = item.position"
      />
    </GmapMap>
    <button @click="test">click</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      center: { lat:  42.8153, lng: 132.8905 },
      mapTypeId: "satellite",
      markers: [
        { position: { lat: 42.8150, lng: 132.8907 }, title: 'Screen5', icon: 'http://maps.google.com/mapfiles/kml/pal3/icon12.png'},
        { position: { lat: 42.8145, lng: 132.8900 }, title: 'Screen6', icon: 'http://maps.google.com/mapfiles/kml/pal3/icon13.png' }
      ],
      info: [{content:'Demendge'}]
    };
  }
};
</script>

<style lang="scss" scoped>
.vue-map-container {
  height: 450px;
  max-width: 992px;
  width: 100%;
}
</style>
