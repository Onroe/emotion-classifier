<template>
      <div class="train">
        <template v-if="mode == 'train'">
            <h1>TRAINING</h1>
        </template>
        <template v-else>
            <h1>TESTING</h1>
        </template>
      <div class="flex">
      <p class="col-md-3">SELECT OPTION:</p>
      <span class="col-md-6">
      <b-form-select   id="use_case" v-on:change="changeOption()" required>
      <!-- These options will appear after the ones from 'options' prop -->
      <b-form-select-option value="train">Train</b-form-select-option>
      <b-form-select-option value="test">Test</b-form-select-option>
      </b-form-select>
      </span>
      </div>
        <Camera></Camera>

        <template v-if="mode == 'train'">
            <div class="flex">
             <span class="col-md-3"><p >SELECT EMOTION TO TRAIN</p></span>
             <span class="col-md-6"><b-form-select v-model="selected" :options="emotions" id="emotionlist"> </b-form-select></span>
             </div>
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
      const img = tf.browser.fromPixels(this.$children[1].webcam.webcamElement);
      const logits = this.mobilenet.infer(img, 'conv_preds');
      this.classifier.addExample(logits, parseInt(this.class, 10));
      console.log(logits);
      // console.log(this.$children[0]);
    },
    async getEmotion() {
      const img = tf.browser.fromPixels(this.$children[1].webcam.webcamElement);
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
    async kerasOption() {
      const model = await tf.loadLayersModel('cnnmodel.json');
      const example = tf.fromPixels(this.$children[0].webcam.webcamElement); // for example
      // const img = tf.browser.fromPixels(this.$children[0].webcam.webcamElement);
      const prediction = model.predict(example);
      console.log(prediction);
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
<style scoped>
div.flex {
    display: flex;
    border: 0px solid black;
    margin: 5px;
    padding: 5px;
}

div > * {
  padding: 0 5px;
}

</style>
