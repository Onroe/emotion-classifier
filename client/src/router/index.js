import Vue from 'vue';
import VueRouter from 'vue-router';
import Index from '../views/Index.vue';
import Camera from '../views/Camera.vue';
import Test from '../views/Test.vue';

Vue.use(VueRouter);

const routes = [

  {
    path: '/index',
    name: 'Index',
    component: Index,
  },
  {
    path: '/camera',
    name: 'Camera',
    component: Camera,
  },
  {

    path: '/test',
    name: 'Test',
    component: Test,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
