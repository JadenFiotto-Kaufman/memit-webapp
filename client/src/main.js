

import Vue from 'vue';
import App from './App.vue';
import router from './router';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import VueGtag from 'vue-gtag';

import 'bootstrap/dist/css/bootstrap.css';
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(router)
Vue.use(VueGtag, {
  config: {id: "G-FD12LWN557"},
}, router)

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');