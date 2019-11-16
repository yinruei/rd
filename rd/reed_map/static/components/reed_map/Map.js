
const ReedMap = {
  name: 'ReedMap',
  props: [
    'markers_info',
    'user_edit_permission'
  ],

  data() {
    return {
      map: null,

      reed_markers: [],
      recycling_markers: [],
      restaurant_markers: [],
      river_markers: [],

      reed_datas: GV.REED_DATAS,
      restaurant_datas: GV.GEEN_RESTAURANT,
      recycling_datas: GV.BEE_HOTEL_DATAS,
      river_datas: [{
        lat: 25.095184,
        lon: 121.611789
      },{
        lat: 24.795184,
        lon: 120.611789
      },{
        lat: 24.095184,
        lon: 120.811789
      },{
        lat: 25.095184,
        lon: 121.611789
      },{
        lat: 24.095184,
        lon: 120.611789
      }]

    }
  },

  computed: {

  },

  methods: {
    map_init() {
      let southWest = L.latLng(21.809023, 119.687789)
      let northEast = L.latLng(25.295184, 122.386521)

      this.map = new L.Map('map', {
          center: new L.LatLng(23.045915, 120.994775),
          zoom: 8,
          maxZoom: 18,
          minZoom: 7,
          maxBounds: L.latLngBounds(southWest, northEast),
      });
      console.log('21222', GV.MAP_TILE)
      this.map.addLayer(new L.TileLayer(GV.MAP_TILE, {
        attribution: '@Google'
      }))

      // this.map.addLayer(new L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      //     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      // }));
    },

    get_context(data) {
      if (data) {
        return data
      }

      return '--'
    },

    get_marker_popup(data, marker_type) {
      let popup_html = ''
      let imgs = ''
      let upload_btn = ''

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
      if (data.hasOwnProperty('img')) {
        imgs = '<img width=600 src="' + data.img + '"/>'
      }

      popup_html += imgs

      if (this.user_edit_permission.hasOwnProperty(GV.USER)) {
        let user_permission = this.user_edit_permission[GV.USER]
        if (user_permission.indexOf(marker_type) >= 0) {
          upload_btn = '<button>我要上傳</button>'
        }
      }

      popup_html += upload_btn

      return popup_html
    },

    add_item_marker(datas, markers, icon, marker_type) {
      for (let data of datas) {
        let marker_popup_info = this.get_marker_popup(data, marker_type)
        let popup_options = {
          'className' : 'custom_marker_popup',
          maxWidth: 700
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
          else if (marker_info.name === 'river') {
            datas = this.river_datas
            markers = this.river_markers
          }

          if (datas !== null && markers !== null) {
            if (marker_info.selected) {
              if (marker_info.name === 'river') {
                this.add_river_markers()
              }
              else {
                this.add_item_marker(datas, markers, marker_info.icon, marker_info.name)
              }
            }
            else {
              this.remove_item_marker(markers)
            }
          }
        }
      }
    },

    add_river_markers() {
      if (this.map !== null) {
        for (let marker_info of this.river_datas) {
          let geojsonMarkerOptions = {
            radius: 8,
            fillColor: "#ff7800",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          }
          let marker = L.circleMarker([marker_info['lat'], marker_info['lon']], geojsonMarkerOptions);
          this.map.addLayer(marker)
          this.river_markers.push(marker)
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