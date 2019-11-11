
const ReedMap = {
  name: 'ReedMap',
  props: [
  ],

  data() {
    return {
      map: null,
      data_info: [{
        'lat': 121.0233,
        'lon': 20.111,
        'info': {
          'footprint': 10,
          'file_path': ''
        }
      }]
    }
  },

  computed: {

  },

  methods: {
    map_init() {
      let southWest = L.latLng(25.295184, 119.687789)
      let northEast = L.latLng(21.809023, 122.386521)

      this.map = new L.Map('map', {
          center: new L.LatLng(23.045915, 120.994775),
          zoom: 8,
          maxZoom: 15,
          minZoom: 7,
          maxBounds: L.latLngBounds(southWest, northEast)
      });

      this.map.addLayer(new L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      }));
    },

    create_marker() {
      let markers = []
      for (let data_info of this.data_info) {
        console.log(data_info.lat, data_info['lat'])
        this.map.addLayer(L.marker([data_info['lat'], data_info['lon']]))
      }
      console.log(this.map, markers)
    }
  },

  mounted() {
    this.map_init()
    this.create_marker()
  },

  watch: {
    data_info() {
      this.create_marker()
    }
  },

  template: `
    <div id="map"></div>
  `
};