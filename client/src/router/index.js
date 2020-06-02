import Vue from 'vue';
import tracking from 'tracking';
import VueRouter from 'vue-router';
import Index from '../views/Index.vue';
import Camera from '../views/WebCam.vue';
import Image from '../views/Picture.vue';

Vue.use(VueRouter, tracking);

const routes = [

  {
    path: '/index',
    name: 'Index',
    component: Index,
  },
  {
    path: '/webcamera',
    name: 'WebCam',
    component: Camera,
  },
  {

    path: '/picture',
    name: 'Picture',
    component: Image,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
