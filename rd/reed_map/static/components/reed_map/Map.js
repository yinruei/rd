
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

      reed_datas: GV.REED_DATAS,
      restaurant_datas: GV.GEEN_RESTAURANT,
      // recycling_datas: [{
      //   lat: 25.095184,
      //   lon: 121.611789
      // },{
      //   lat: 24.795184,
      //   lon: 120.611789
      // },{
      //   lat: 24.095184,
      //   lon: 120.811789
      // },{
      //   lat: 25.095184,
      //   lon: 121.611789
      // },{
      //   lat: 24.095184,
      //   lon: 120.611789
      // }]
      recycling_datas: GV.BEE_HOTEL_DATAS

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
          maxZoom: 18,
          minZoom: 7,
          maxBounds: L.latLngBounds(southWest, northEast),
      });

      this.map.addLayer(new L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      }));
    },

    get_context(data) {
      if (data) {
        return data
      }

      return '--'
    },

    get_marker_popup(data) {
      let popup_html = ''
      if (data.hasOwnProperty('name')) {
        popup_html += '<div>名稱: ' + this.get_context(data.name) + '</div>'
      }
      if (data.hasOwnProperty('address')) {
        popup_html += '<div>地址: ' + this.get_context(data.address) + '</div>'
      }
      if (data.hasOwnProperty('bussiness_time')) {
        popup_html += '<div>營業時間: ' + this.get_context(data.bussiness_time) + '</div>'
      }
      if (data.hasOwnProperty('updtime')) {
        popup_html += '<div>更新時間: ' + this.get_context(data.updtime) + '</div>'
      }

      return popup_html
    },

    add_item_marker(datas, markers, icon) {
      for (let data of datas) {
        let marker_popup_info = this.get_marker_popup(data)
        let popup_options = {
          'className' : 'custom_marker_popup'
        }
        let marker = L.marker([data['lat'], data['lon']], {icon: icon}).bindPopup(marker_popup_info, popup_options)
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
          else if (marker_info.name === 'recycling') {
            datas = this.recycling_datas
            markers = this.recycling_markers
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