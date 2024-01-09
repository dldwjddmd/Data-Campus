<template>
    <div class="text-start mx-auto mp-auto overflow-scroll" style="border: 0.01rem solid; height: 10.0rem; width: 40.0rem; font-family: 'LeferiPoint-WhiteObliqueA'; font-size: 0.5rem;">
        "영상을 시작합니다.." <br />
        <span v-for="log in logs">{{format(log)}}<br /></span>
    </div>
</template>

<script lang="ts">
export default {
    "name": "Description",
}
</script>

<script lang="ts" setup>
import {Ref, inject, ref, watch} from 'vue';

import {Log} from '../types';

const latestLog: Ref<Log| null> = inject("latestLog", ref(null));

const logs: Ref<Log[]> = ref([]);

watch(latestLog, (cur: Ref<Log | null> , prv: Ref<Log | null>) => {
    if(latestLog && latestLog.value) {
        logs.value.push(latestLog.value);
    } else {
        // 정리하기
        logs.value = [];
    }
});

const format = (log:Log):string => {
    let msg:string = "";
    msg += `[ ${log.recorded} ] `;
    msg += `[ 위험도: `;
    if(log.risk == 0) {
        msg += '낮음';
    } else if(log.risk == 1) {
        msg += '주의';
    } else {
        msg += '위험';
    }
    msg += ' ] ';

    const objCounts:{[key: string]: number} = {"bicycle": 0, "motorcycle": 0, "kickboard": 0};

    for(let obj of log.objects) {
        objCounts[obj.category] += 1;
    }
    msg += `[ 자전거: ${objCounts["bicycle"]}개, 오토바이: ${objCounts["motorcycle"]}, 킥보드: ${objCounts["kickboard"]} ] `;
    
    if(log.risked.length > 0) {
        msg += `[ 위험물:`;
        for(let idx of log.risked) {
            msg += ` ${log.objects[idx]} `;
        }
        msg += '] ';
    }
    return msg;
}
            
</script>