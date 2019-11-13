
const Aside = {
  name: 'Aside',
  props: [
    'markers_info'
  ],

  data() {
    return {
    }
  },

  computed: {

  },

  methods: {
  },

  mounted() {
  },

  watch: {
  },

  template: `
    <div>
      <div
        class="marker_btn_container"
      >
        <div
          v-for="(marker_info, _idx) in markers_info"
        >
          <div
            :key="'marker_type'+_idx"
            class="marker_btn"
          >
            <input
              type="checkbox"
              :key="'option-checkbox' + _idx"
              :id="'option-checkbox'+ _idx"
              class="u-hide"
              v-model="marker_info.selected"
            >
            <label
              class="btn btn-long btn_white"
              :for="'option-checkbox' + _idx"
              :key="'option-checkbox-label' + _idx"
            >
              <img
                :src="marker_info.img"
              >
            </label>
          </div>
        </div>
      </div>
    </div>
  `
};