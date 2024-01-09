<template>

<div class="container">
    <div class="row">
        <div class="col">
            <button type="button" class="btn btn-success mx-auto my-3" data-bs-toggle="modal" data-bs-target="#exampleModal" style="width:20rem">
                서비스 이용하기
            </button>
        </div>
        <div class="col">
            <div class="input-group mx-auto my-3" style="width:20rem">
                <input type="text" class="form-control" placeholder="영상 이름" aria-label="영상 이름" aria-describedby="basic-addon2" v-model="title"/>
                <div class="input-group-append">
                    <button class="btn btn-secondary" type="button" @click.prevent="startVideo">재생</button>
                </div>
            </div>
        </div>
  </div>
<!-- Button trigger modal -->

</div>
<!-- Modal -->
<div class="modal" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="false">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">서버 주소를 입력해주세요</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
            <input type="url" class="form-control" id="serverAddr" v-model="_server" aria-describedby="urlHelp" required aria-required="true" placeholder="http://localhost:9000">
            <div id="urlHelp" class="form-text">서버 주소는 라즈베리 파이 주소입니다</div>
        </div>
        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal" @click="connectServer();">Submit</button>
      </div>
    </div>
  </div>
</div>
<main class="px-auto text-center mx-auto" style="width:40rem">
    <div class="container px-0 my-1">
        <div class="row">
            <div class="col-sm-2">
            </div>
            <div class="col">
                <h5 class = "pb-0 pt-2 mb-0 mt-1">{{video?.title ? video.title : "우리는 곰돌이팀!"}}</h5>
            </div>
            <div class="col-sm-2 float-bs">
                <button type="button" class="btn btn-light pt-2 pb-1" style="float:right" @click.prevent="endVideo">종료</button>
            </div>
        </div>
    </div>
    <screen></screen>
    <description></description>
    
</main>
</template>


<script lang="ts">
export default {
    name: 'Demo',
}

</script>

<script lang="ts" setup>
import axios, {AxiosResponse} from 'axios';
import {ref, Ref, provide, watch} from 'vue';

import Screen from './Screen.vue';
import Description from './Description.vue';
import {RawVideo, Log, RawImage} from '../types';

const _server:Ref<string> = ref("");
const server:Ref<string> = ref("");
const connected:Ref<boolean> = ref(false);

const video: Ref<RawVideo | null> = ref(null);
const latestLog: Ref<Log | null> = ref(null);
const receivedImg:Ref<RawImage | null > = ref(null);

const title:Ref<string> = ref("");

const connectServer = () => {
    server.value = _server.value;
    axios.get(server.value)
        .then((res:AxiosResponse) => {
            console.log("서버 연결 성공");
            alert("서버에 연결되었습니다.");
            connected.value = true;
        })
        .catch((reson) => {
            console.log("연결 실패!!!");
            console.log(reson);
            alert("서버 연결을 실패했습니다.");
            connected.value = false;
        })
        .finally(()=> {
            console.log(server)
            _server.value = "";
        });
};

const startVideo = () => {
    if(connected) {
        if(title.value.length > 0){
        axios.post(server.value + `/video/${title.value}/start`)
            .then((ret:AxiosResponse) => {
                video.value = ret.data;
                return axios.post(server.value + `/log/${title.value}/start`);
            })
            .then((ret:AxiosResponse) => {
                latestLog.value = ret.data;
                alert("영상을 시작합니다.");
            })
            .catch((reason) => {
                console.log(reason);
                alert("영상을 시작할 수 없습니다.");
            })
            .finally(() => title.value = "");
        } else {
            alert("유효한 제목을 입력해주세요.");
        }
    } else {
        alert("서버에 연결되지 않았습니다!");
    }
};

const endVideo = () => {
    if(connected) {
        axios.post(server.value + `/video/${video.value?.title}/end?savedTitle=recorded`)
            .then((ret:AxiosResponse) => {
                return axios.post(server.value + `/log/${video.value?.title}/end?savedTitle=recorded`);
            })
            .then((ret:AxiosResponse) => {
                alert("영상을 종료합니다.");
            })
            .catch((reason) => {
                console.log(reason);
                alert("영상을 종료할 수 없습니다.");
            })
            .finally(() => {
                video.value = null;
                latestLog.value = null;
                title.value = "";
            });
    } else {
        alert("서버에 연결되지 않았습니다!");
    }
}

watch(latestLog, async (cur:Ref<Log | null>, prv:Ref<Log | null>) => {
    if(latestLog && latestLog.value != null) {
        //start Video
        try {
            await startVideoStreaming();
        } catch(reason) {
            console.log(reason);
        }
    }
})

const startVideoStreaming = async () => {
    while(video.value && connected.value && server.value.length != 0) {
        try {
            let ret:AxiosResponse = await axios.get(server.value + `/video/${video.value.title}/streaming`);
            receivedImg.value = ret.data;

            if(receivedImg.value) {
                ret = await axios.post(server.value + `/log/${video.value.title}/prediction`, JSON.stringify(receivedImg.value), {
                    headers: { "Content-Type": `application/json`},
                });
                latestLog.value = ret.data;

                // Save Frame
                // ret = await axios.post(server.value + `/video/${video.value.title}/save`, JSON.stringify(receivedImg.value), {
                //     headers: { "Content-Type": `application/json`},
                // });
                // ret = await axios.post(server.value + `/log/${video.value?.title}/save`);
                // console.log(`Frame: ${receivedImg.value.id}`);
            } else {
                console.log("받은 이미지가 없습니다.");
            }
        } catch(reason) {
            console.log(reason);
            // alert("영상을 받는데 실패했습니다.");
        }
    }
    //화면 정리
    console.log(`video: ${video.value}\nconnected: ${connected.value}\nserver: ${server.value}`);
    receivedImg.value = null;
    latestLog.value = null;
};

provide("video", video);
provide("latestLog", latestLog);
provide("receivedImg", receivedImg);
</script>

<style scoped>
h5{
  font-family:"LeferiPoint-WhiteObliqueA";
  font-size:1.5rem;
}

div.col{
    font-family:"LeferiPoint-WhiteObliqueA";
}
.btn{
    font-family:"LeferiPoint-WhiteObliqueA";
}
</style>