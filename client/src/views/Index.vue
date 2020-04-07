<template>
      <div class="train">
        <template v-if="mode == 'train'">
            <h1>TRAIN</h1>
        </template>
        <template v-else>
            <h1>TEST MODEL</h1>
        </template>
        <Camera></Camera>
        <b-form-select   id="use_case" :required="true" v-on:change="changeOption()">
      <!-- This slot appears above the options from 'options' prop -->
      <template v-slot:first>
        <b-form-select-option :value="null" disabled >Please select an option</b-form-select-option>
      </template>
      <!-- These options will appear after the ones from 'options' prop -->
      <b-form-select-option value="train">Train</b-form-select-option>
      <b-form-select-option value="test">Test</b-form-select-option>
    </b-form-select>

        <template v-if="mode == 'train'">
             <b-form-select v-model="selected" :options="emotions" id="emotionlist">
            </b-form-select>
            <b-button  variant="outline-primary" v-on:click="trainModel()">Train Model</b-button>
        </template>
        <template v-else>
            <b-button variant="success" v-on:click="getEmotion()">Get Emotion</b-button>
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
      selected: null,
      emotions: [{ value: 'angry', text: 'angry' }, { value: 'happy', text: 'happy' }],
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
      // console.log(this.$children[0]);
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
