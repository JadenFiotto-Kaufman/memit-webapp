import Vue from 'vue';
import Router from 'vue-router';

import LLME from '../components/LLME.vue'
import LLME_Help from '../components/Help.vue'

Vue.use(Router);


const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'LLME',
      component: LLME,

      meta:{
        title: "Memit Explorer"
      }
    },
    {
      path: '/help',
      name: 'LLME_Help',
      component: LLME_Help,
      meta:{
        title: "Whats This?"
      }
    },
  ],
});

router.afterEach((to, from) => {
  // Use next tick to handle router history correctly
  // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
  Vue.nextTick(() => {
      document.title = to.meta.title || "Memit Explorer";
  });
});

export default router;