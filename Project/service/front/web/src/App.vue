<template>
    <nav-bar />
    <router-view />
    <info />
</template>

<script lang="ts">
export default {
  name: 'App',
};
</script>

<script lang="ts" setup>
import { Ref, ref, provide, reactive } from 'vue';
import { Page } from './types';

const pages: {[page: string]:Page} = reactive({
    'home': {
        key: 0,
        url: '/home',
        name: 'INTRO',
    },
    'demo': {
        key: 1,
        url: '/demo',
        name: 'TRY',
    },
    'profile': {
        key: 2,
        url: '/profile',
        name: 'TEAM INFO',
    },
});
const currentPage:Ref<Page> = ref(pages.home);

const onFocus = (evt:Event, page:Page) => {
    // console.log(evt.currentTarget);
    currentPage.value = page;
}

provide('pages', pages);
provide('currentPage', currentPage);
provide('onFocus', onFocus);

</script>
