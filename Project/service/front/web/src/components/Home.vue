<template>
<main class="px-3">
    <div class="container text-center">
        <div class="row ">
            <!--div class="col">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqjssvHhbkoqeRInsMnFYPok6J13tFCalvhze2ZHON5hUJVs9De8_nhpGtrQflN7ifmBw&amp;usqp=CAU" alt="two men riding bicycle" style="width:20.0rem; height 25.0rem; margin-top: 4.0rem;">
            </div-->
            <div class="col">
                <h1 class="fw-bold" style="font-family:'KOTRA_BOLD-Bold'; font-size:3.0rem; margin-bottom: 0.3rem; padding-bottom: 0.0rem;">ISUB</h1>
                
                <p class="lead" align="left" style="margin-top: 0.0rem; padding-top:0.0rem;"> 
                    <span class="isub">I'll See U'r Back(ISUB)</span>의 줄임말로, <br/>
                    저희의 서비스는 자전거 이용자들의 후방 충돌을 방지해 안전을 지켜주는 서비스입니다.<br/>
                    후방 좌측 / 우측에서 다가오는 자전거, 전동 킥보드, 오토바이를 탐지해 위험도를 시각화해주며 이용자가 빠른 대처를 할 수 있도록 예방할 수 있습니다.<br/>
            
                
                </p>
                <router-link to="/demo" class="try btn btn-lg btn-secondary fw-bold border-white bg-white" @click.prevent="onFocus($event, pages.demo)" align="center">TRY IT</router-link>
            </div>
        </div>
    </div>
</main>
</template>

<script lang="ts">
export default {
    name: 'Home',
}
</script>

<script lang="ts" setup>
import { inject } from 'vue';
import { Page } from '../types';

const pages:{[page:string]:Page} = inject('pages', {});
const onFocus:(evt:Event, page:Page)=>void = inject('onFocus', (evt:Event, page:Page) => {});
</script>

<style scoped>
/* Custom default button */
.btn-secondary,
.btn-secondary:hover,
.btn-secondary:focus {
  color: #333;
  text-shadow: none; /* Prevent inheritance from `body` */
}

.try{
    font-family:"KOTRA_BOLD-Bold";
}

.lead{
    font-family:"LeferiPoint-WhiteObliqueA";
    font-size:18px;
}

.isub{
    font-family:"GowunDodum-Regular";
    font-style:"solid";
}
</style>