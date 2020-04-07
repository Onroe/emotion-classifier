<template>
      <div class="train">
        <template v-if="mode == 'train'">
            <h1>TRAIN</h1>
        </template>
        <template v-else>
            <h1>TEST MODEL</h1>
        </template>
        <select id="use_case" v-on:change="changeOption()">
            <option value="train">Train</option>
            <option value="validate">Validate</option>
        </select>
        <Camera></Camera>
        <template v-if="mode == 'train'">
            <select id="emotionlist">
                <template v-for="(emotion, index) in emotions">
                    <option :key="index" :value="index">{{emotion}}</option>
                </template>
            </select>
            <button v-on:click="trainModel()">Train Model</button>
        </template>
        <template v-else>
            <button v-on:click="getEmotion()">Get Emotion</button>
        </template>
        <h1>{{ detected_e }}</h1>
      </div>
</template>
<script>
// @ is an alias to /src
import Camera from '@/views/Camera.vue';
import * as tf from '@tensorflow/tfjs';
import * as mobilenetModule from '@tensorflow-models/mobilenet';
import * as knnClassifier from '@tensorflow-models/knn-classifier';
import axios from 'axios';

export default {
  name: 'Index',
  components: {
    Camera,
  },
  data() {
    return {
      emotions: ['angry', 'happy'],
      classifier: null,
      mobilenet: null,
      class: null,
      detected_e: null,
      mode: 'train',
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    async init() {
      // load the load mobilenet and make a KnnClassifier
      this.classifier = knnClassifier.create();
      this.mobilenet = await mobilenetModule.load();
    },
    trainModel() {
      const selected = document.getElementById('emotionlist');
      this.class = selected.options[selected.selectedIndex].value;
      this.addSample();
    },
    addSample() {
      const img = tf.browser.fromPixels(this.$children[0].webcam.webcamElement);
      const logits = this.mobilenet.infer(img, 'conv_preds');
      this.classifier.addExample(logits, parseInt(this.class, 10));
      console.log(logits);
    },
    async getEmotion() {
      const img = tf.browser.fromPixels(this.$children[0].webcam.webcamElement);
      const logits = this.mobilenet.infer(img, 'conv_preds');
      const pred = await this.classifier.predictClass(logits);
      console.log(pred);
      this.detected_e = this.emotions[pred.classIndex];
      this.recordEmotion();
    },
    changeOption() {
      const selected = document.getElementById('use_case');
      this.mode = selected.options[selected.selectedIndex].value;
    },
    recordEmotion() {
      axios.post('http://localhost:5000/server/', {
        emotion: this.detected_e,
      }).then(() => {
        alert('Xiexie for recording your emotion');
      });
    },
  },
};
</script>
