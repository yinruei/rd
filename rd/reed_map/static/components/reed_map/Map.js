
const ReedMap = {
  name: 'ReedMap',
  props: [
    'markers_info',
  ],

  data() {
    return {
      map: null,

      reed_markers: [],
      recycling_markers: [],
      restaurant_markers: [],

      reed_datas: [
        {
          'lat': 23.045915,
          'lon': 120.994775,
        },
      ],

      restaurant_datas: GV.GEEN_RESTAURANT
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
          maxBounds: L.latLngBounds(southWest, northEast),
          // layers: [
          //   this.base_layers[this.base_layer]
          // ]
      });

      this.map.addLayer(new L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      }));
    },

    add_item_marker(datas, markers, icon) {
      for (let data of datas) {
        let marker = L.marker([data['lat'], data['lon']], {icon: icon})
        this.map.addLayer(marker)
        markers.push(marker)
      }
    },

    remove_item_marker(markers) {
      for (let marker of markers) {
        this.map.removeLayer(marker)
      }
      markers = []
    },

    setup_markers(markers_datas) {
      if (this.map !== null) {
        for (let marker_info of markers_datas) {
          let datas = null
          let markers = null

          if (marker_info.name === 'reed') {
            datas = this.reed_datas
            markers = this.reed_markers
          }
          else if (marker_info.name === 'green_restaurant') {
            datas = this.restaurant_datas
            markers = this.restaurant_markers
          }

          if (datas !== null && markers !== null) {
            if (marker_info.selected) {
              this.add_item_marker(datas, markers, marker_info.icon)
            }
            else {
              this.remove_item_marker(markers)
            }
          }
        }
      }
    }
  },

  mounted() {
    this.map_init()
    this.setup_markers(this.markers_info)
  },

  watch: {
    data_info() {
      // this.create_marker()
    },

    markers_info: {
      handler(new_markers_info, old_info) {
        this.setup_markers(new_markers_info)
      },
      deep: true,
      immediate: true
    }
  },

  template: `
    <div id="map"></div>
  `
};