<template>
<main class="px-3">
    <div class="m-portlet__body">
        <p class="info">&lt 팀원정보 &gt</p>
        <div class="row" style="text-align:center;" font-size="0.6rem">
            <div v-for="profile in profiles" :key="profile.key" class="col-md-4" style="margin-bottom: 2.0rem; margin-top: 2.0rem;">
                <img class="certificate" :title="profile.name" :src="profile.url" style="width:10.0rem;height:10.0rem; margin-bottom: 0.5rem;"/>
                <br/>
                {{profile.name}}
                <br/>
                {{profile.email}}
                <br />
                {{profile.role}}
            </div>
        </div>
    </div>
</main>
</template>

<script lang="ts">
export default {
    name: 'Profile',
}
</script>

<script lang="ts" setup>
import {reactive} from 'vue';
import {Profile} from '../types';

const profiles:Profile[] = reactive([
    {key: 0, name: '배채은', url: 'src/assets/profiles/chaeeun.png', email: 'bchaeeun9@naver.com', role: '개발&학습'},
    {key: 1, name: '박채나', url: 'src/assets/profiles/chaena.png', email: 'chaena7@gmail.com', role: '개발&학습'},
    {key: 2, name: '이정은', url: 'src/assets/profiles/jeongeun.png', email: 'wheeboo@naver.com', role: '개발&학습'},
    {key: 3, name: '정인호', url: 'src/assets/profiles/inho.png', email: 'inhovation97@gmail.com', role: '개발&학습'},
    {key: 4, name: '윤영로', url: 'src/assets/profiles/yeongro.png', email: 'appleofyyr@icloud.com', role: '개발&학습'},
]);
</script>

<style>
.row{
    font-family:"GowunDodum-Regular";
}
.info{
    font-family:"LeferiPoint-WhiteObliqueA";
}
</style>
