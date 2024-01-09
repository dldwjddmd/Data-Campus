<template>
    <div class="embed-responsive embed-responsive-1by1">
        <canvas id="screen" ref="canvas">
        최신 버전의 크롬을 이용해주세요!
        </canvas>
        <!-- <video src="../../demo/demo01.mp4" autoplay controls></video> -->
        
    </div>
</template>

<script lang="ts">
export default {
    name: "Screen",
}
</script>

<script lang="ts" setup>
import {ref, Ref, onMounted, inject, watch} from 'vue';

import {RawVideo, RawImage, Log, RawObject} from '../types';

const video: Ref<RawVideo | null> = inject("video", ref(null));
const latestLog: Ref<Log| null> = inject("latestLog", ref(null));
const receivedImg: Ref<RawImage| null> = inject("receivedImg", ref(null));

const canvas:Ref<HTMLCanvasElement | null> = ref(null);
const ctx:Ref<CanvasRenderingContext2D | null> = ref(null);

const imgData: Ref<ImageData> = ref(new ImageData(1, 1));

onMounted(() => {
    ctx.value = canvas.value?.getContext("2d") as CanvasRenderingContext2D;
});

let width: number = 1;
let height: number = 1;
watch(video, async (cur:Ref<RawVideo | null>, old:Ref<RawVideo | null>) => {
    if(video && video.value && ctx.value) {
        width = video.value.width;
        height = video.value.height;

        imgData.value = ctx.value.createImageData(width, height);
    }
});

watch(receivedImg, async (cur:Ref<RawImage | null>, prv: Ref<RawImage | null>) => {
    if(receivedImg && receivedImg.value != null) {
        try {
            await setImage();
        } catch(reason) {
            console.log(reason);
        }
    } else {
        imgData.value.data.fill(0);
        ctx.value?.putImageData(imgData.value, 0, 0);
    }
});

const setImage = async () => {
    if(video.value && ctx.value && receivedImg.value) {
        const bytes = Uint8Array.from(atob(receivedImg.value.data), c => c.charCodeAt(0));
        imgData.value.colorSpace

        let t = 0;
        for (let i = 0; i < imgData.value.data.length; i += 4) {
            // Modify pixel data
            imgData.value.data[i + 0] = bytes[t + 0];        // R value
            imgData.value.data[i + 1] = bytes[t + 1];        // G value
            imgData.value.data[i + 2] = bytes[t + 2];        // B value
            imgData.value.data[i + 3] = 255;                  // A value
            t += 3;
        }
        ctx.value.putImageData(imgData.value, 0, 0);
        return true;
    }  else {
        return Promise.reject(`video: ${video.value}\nctx: ${ctx.value}\nreceivedImg: ${receivedImg.value}`);
    }
};

// 다가오는 방향 확인
watch(latestLog, (cur:Ref<Log | null>, prv:Ref<Log | null>) => {
    if(latestLog && latestLog.value && ctx.value && canvas.value) {
        ctx.value.fillStyle = 'red';

        const alpha = {"low": 0.0, "mid": 0.3, "high": 0.6};
        const riskedAlpha: {[key:string]:number} = {"left": 0.0, "center": 0.0, "right": 0.0};
        
        let pos: number;
        let obj: RawObject;
        for(let idx of latestLog.value.risked) {
            obj = latestLog.value.objects[idx];
            pos = obj.center[0];
            
            if(pos < 1 / 3) {
                if(obj.risk == 0 && riskedAlpha["left"] < alpha["low"]) {
                    riskedAlpha["left"] = alpha["low"];
                } else if(obj.risk == 1 && riskedAlpha["left"] < alpha["mid"]) {
                    riskedAlpha["left"] = alpha["mid"];
                } else if(obj.risk == 2 && riskedAlpha["left"] < alpha["high"]) {
                    riskedAlpha["left"] = alpha["high"];
                }
            }
            else if(pos < 2 / 3) {
                if(obj.risk == 0 && riskedAlpha["center"] < alpha["low"]) {
                    riskedAlpha["center"] = alpha["low"];
                } else if(obj.risk == 1 && riskedAlpha["center"] < alpha["mid"]) {
                    riskedAlpha["center"] = alpha["mid"];
                } else if(obj.risk == 2 && riskedAlpha["center"] < alpha["high"]) {
                    riskedAlpha["center"] = alpha["high"];
                }
            }  else {
                    if(obj.risk == 0 && riskedAlpha["right"] < alpha["low"]) {
                        riskedAlpha["right"] = alpha["low"];
                    } else if(obj.risk == 1 && riskedAlpha["right"] < alpha["mid"]) {
                        riskedAlpha["right"] = alpha["mid"];
                    } else if(obj.risk == 2 && riskedAlpha["right"] < alpha["high"]) {
                        riskedAlpha["right"] = alpha["high"];
                }
            }
        }
        ctx.value.globalAlpha = riskedAlpha["left"];
        ctx.value.fillRect(0, 0, canvas.value.width / 3, canvas.value.height);

        ctx.value.globalAlpha = riskedAlpha["center"];
        ctx.value.fillRect(canvas.value.width / 3, 0, canvas.value.width / 3, canvas.value.height);

        ctx.value.globalAlpha = riskedAlpha["right"];
        ctx.value.fillRect(2 * canvas.value.width / 3, 0, canvas.value.width / 3, canvas.value.height);
        
        //init
        ctx.value.globalAlpha = 1.0;
    }});
</script>

<style scoped>
canvas, video {
    border: 0.1rem solid #fff; 
    height: 20rem; 
    width: 40rem;
    /* height: 13rem;
    width: 8rem; */
}
</style>