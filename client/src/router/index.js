import Vue from 'vue';
import Router from 'vue-router';

import LogitLens from '../components/LogitLens.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/logitlens',
      name: 'LogitLens',
      component: LogitLens,
    },
  ],
});