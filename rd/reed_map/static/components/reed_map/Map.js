
const CctvMap = {
  name: 'CctvMap',
  props: [
  ],

  data() {
    return {
      map: null,
    }
  },

  computed: {

  },

  methods: {
    map_init() {
      let southWest = L.latLng(18.20, 105.85)
      let northEast = L.latLng(30.20, 135.85)

      this.map = new L.Map('map', {
          center: new L.LatLng(23.045915, 120.994775),
          zoom: 11,
          maxZoom: 15,
          minZoom: 7,
          maxBounds: L.latLngBounds(southWest, northEast)
      });

      this.map.addLayer(new L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      }));
    }
  },

  mounted() {
    this.map_init()
  },

  watch: {
  },

  template: `
    <div id="map"></div>
  `
};