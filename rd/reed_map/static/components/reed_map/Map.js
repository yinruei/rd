
const ReedMap = {
  name: 'ReedMap',
  props: [
    'markers_info',
    'user_edit_permission'
  ],

  data() {
    return {
      map: null,
      selected_marker: null,
      select_marker_id: null,

      reed_markers: [],
      recycling_markers: [],
      restaurant_markers: [],
      river_markers: [],

      reed_datas: GV.REED_DATAS,
      restaurant_datas: GV.GEEN_RESTAURANT,
      recycling_datas: GV.BEE_HOTEL_DATAS,
      river_datas: GV.RIVER_DATAS

    }
  },

  computed: {

  },

  methods: {
    map_init() {
      let southWest = L.latLng(21.809023, 119.687789)
      let northEast = L.latLng(30.295184, 122.386521)

      this.map = new L.Map('map', {
          center: new L.LatLng(23.045915, 120.994775),
          zoom: 8,
          maxZoom: 18,
          minZoom: 7,
          maxBounds: L.latLngBounds(southWest, northEast),
      });

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
      let popup_html = '<div class="my_popup_container">'
      let imgs = ''
      let img = ''
      let upload_btn = ''
      let img_width = 600

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
      if (data.hasOwnProperty('img') && marker_type !== 'green_restaurant') {
        img = '<div><img width=600 src="' + data.img + '"/></div>'
        popup_html += img
      }
      if (data.hasOwnProperty('imgs') && marker_type !== 'green_restaurant') {
        for (let _img of data.imgs) {
          imgs += '<div><img width=' + img_width + ' src="' + _img + '"/></div>'
        }
        popup_html += imgs
      }
      if (data.hasOwnProperty('river')) {
        let river_img = ''
        popup_html += '<div style="font-size: 18px;">對應的附近水質測站</div>'

        if (data.river.hasOwnProperty('name')) {
          popup_html += '<div>水質測站名稱：' + data.river.name + '</div>'
        }
        if (data.river.hasOwnProperty('pollution_index')) {
          let quality = ''
          if (data.river.pollution_index < 2) {
            quality ='低'
          }
          else if (data.river.pollution_index <= 6) {
            quality = '中'
          }
          else {
            quality = '高'
          }
          popup_html += '<div>河川汙染指數：' + quality + '</div>'
        }

        for (let _img of data.river.imgs) {
          river_img += '<div><img width=' + img_width + ' src="' + _img + '"/></div>'
        }
        popup_html += river_img

        if (data.river.hasOwnProperty('station_url')) {
          popup_html += '<div><a href="' + data.river.station_url + '" target="_blank">測站連結</a></div>'
        }
      }


      if (this.user_edit_permission.hasOwnProperty(GV.USER)) {
        let user_permissions = this.user_edit_permission[GV.USER]

        if (user_permissions.edit.indexOf(marker_type) >= 0) {
          upload_btn = '<a href="/upload/' + marker_type + '/' + data.id + '/' + GV.USER + '/">我要上傳</a>'
          popup_html += upload_btn
        }
      }

      return popup_html + '</div>'
    },

    add_item_marker(datas, markers, icon, marker_type) {
      let self = this
      for (let data of datas) {
        let marker_popup_info = this.get_marker_popup(data, marker_type)
        let popup_options = {
          'className' : 'custom_marker_popup',
          maxWidth: 750,
          maxHeight: 300
        }
        let marker = L.marker([data['lat'], data['lon']], {icon: icon, datas: data})
                      .bindPopup(marker_popup_info, popup_options)
                      .on('click', (e) => {
                        self.selected_marker = marker_type
                        self.select_marker_id = marker_type + e.target.options.datas.id
                      })
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
        for (let data of this.river_datas) {
          let quality = data['river_pollution_index']

          let icon_img = ''
          // 水質(1~10)分三類<2(未/稍受汙染)、2~6(已受汙染)、>6(嚴重汙染)
          if (quality < 2) {
            icon_img = GV.NORMAL_WATER_ICON
          }
          else if (quality <= 6) {
            icon_img = GV.MID_WATER_ICON
          }
          else {
            icon_img = GV.BAD_WATER_ICON
          }

          let icon = L.icon({
            iconUrl: icon_img,
            // iconSize: [46, 36],
            iconAnchor: [23, 18]
          })
          let marker = L.marker([data['lat'], data['lon']], {icon: icon, datas: data})
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