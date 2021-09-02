import "@fortawesome/fontawesome-free/scss/fontawesome.scss";
import "@fortawesome/fontawesome-free/scss/solid.scss";

import Vue from "vue";
import VueTimers from "vue-timers";
import App from "./App.vue";

Vue.use(VueTimers);
Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App),
  data: { debug: Vue.config.devtools },
}).$mount("#app");
