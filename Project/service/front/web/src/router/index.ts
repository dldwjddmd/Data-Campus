import Profile from '/@components/Profile.vue'
import Home from '/@components/Home.vue';
import Demo from '/@components/Demo.vue'

import { defineComponent } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

const NotFound = defineComponent({
    template: '<div>Not Found</div>',
});
const routes = [
    { path: '/', redirect: '/home'},
    { path: '/home', name: 'home', component: Home},
    { path: '/demo', name: 'demo', component: Demo},
    { path: '/profile', name: 'profile', component: Profile},
    { path: '/:catchAll(.*)+', component: NotFound},
];

export const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: 'active',
    routes,
});