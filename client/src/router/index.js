import Vue from 'vue';
import Router from 'vue-router';

import LLME from '../components/LLME.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'LLME',
      component: LLME,
    },
  ],
});