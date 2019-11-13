
const ReedMap = {
  name: 'ReedMap',
  props: [
    'markers_info'
  ],

  data() {
    return {
      map: null,

      reed_markers: [],
      recycling_markers: [],
      store_markers: [],

      reed_datas: [
        {
          'lat': 23.045915,
          'lon': 120.994775,
        },
      ],
      recycling_datas: [
        {
          'lat': 23.145915,
          'lon': 119.994775,
        },
        {
          'lat': 24.345915,
          'lon': 120.994775,
        },
      ],

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
        console.log([data['lat'], data['lon']], icon)
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

    create_marker() {
      this.add_item_marker(this.reed_datas, this.reed_markers, this.markers_info.reed_icon)

      // for (let recycling_data of this.recycling_green_datas) {
      //   L.marker([recycling_data['lat'], recycling_data['lon']], {icon: IconInfo.recycling_green_icon}).addTo(this.map)
      // }

      // for (let recycling_data of this.recycling_gray_datas) {
      //   L.marker([recycling_data['lat'], recycling_data['lon']], {icon: IconInfo.recycling_gray_icon}).addTo(this.map)
      // }

    }
  },

  mounted() {
    // 沒有map init 就先呼叫到watch的markers_info ＱＱＱＱＱ
    this.map_init()
    console.log("after init")
    this.create_marker()
  },

  watch: {
    data_info() {
      // this.create_marker()
    },

    markers_info: {
      handler(new_markers_info, old_info) {
        if (this.map !== null) {
          for (let marker_info of new_markers_info) {
            let datas = null
            let markers = null

            if (marker_info.name === 'reed') {
              datas = this.reed_datas
              markers = this.reed_markers
            }
            else if (marker_info.name === 'recycling') {
              datas = this.reed_datas
              markers = this.reed_markers
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
      },
      deep: true,
      immediate: true
    }
  },

  template: `
    <div id="map"></div>
  `
};