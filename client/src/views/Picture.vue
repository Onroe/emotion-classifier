<template>
 <div>
  <div class="demo-title">
    <p><a href="" target="_parent"></a>FACIAL EMOTION CLASSIFICATION</p>
  </div>
     <div class="row" id="card-item-container">
        <div class="col s12 m6">
          <div class="card">
            <div id="image-container" class="card-content">
              <div class="demo-container">
                <img id="img" src="../assets/tuwa.jpg" crossOrigin="Anonymous" />
              </div>
            </div>
          </div>
        </div>
  </div>
 </div>
</template>
<script>
import 'tracking/build/tracking-min';
import 'tracking/build/data/face';
import 'tracking/build/data/eye';
import 'tracking/build/data/mouth';
import $ from 'jquery';
import * as tf from '@tensorflow/tfjs';
import Chart from 'chart.js';


const { tracking } = window;
let COUNT_FACE = 0;
let MODEL_EMOTION;
let IS_MODEL_EMOTION_LOADED = false;
const LABEL_EMOTIONS = {
  0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral',
};

export default {
  name: 'picture',
  components: {
  },
  data() {
    return {
      selected: null,

    };
  },
  mounted() {
    this.initEmotion();
  },
  methods: {
    tracking() {
      var img = document.getElementById('img');
      var tracker = new tracking.ObjectTracker(['face']);
      tracker.setStepSize(1.7);
      tracker.setEdgesDensity(0.2);
      tracking.track('#img', tracker);
      console.log('load');
      var vue = this;
      tracker.on('track', function (event) {
        event.data.forEach(function (rect) {
          console.log(rect);
          const face_id = `face_${++COUNT_FACE}`;
          const container_padding_top = 10;
          const container_padding_left = 10;
          const top = rect.y;
          const left = rect.x;
          const { width } = rect.width;
          const { height } = rect.height;
          var rects = document.createElement('div');
          document.querySelector('.demo-container').appendChild(rects);
          rects.classList.add('rects');
          rects.style.position = 'absolute';
          rects.style.width = `${rect.width}px`;
          rects.style.height = `${rect.height}px`;
          rects.style.left = `${img.offsetLeft + left}px`;
          rects.style.top = `${img.offsetTop + top}px`;
          console.log(face_id);
          console.log('START');
          vue.cropFace(rect, face_id);
          const result_emotion = vue.getEmotion(document.getElementById(face_id), face_id);
          console.log(result_emotion);
          vue.generateResultChart(face_id, result_emotion);
          vue.clearFaceCanvas();
        });
      });
    },
    async initEmotion() {
      const Url = 'http://localhost/track/model/emotion/model.json';
      MODEL_EMOTION = await tf.loadLayersModel(Url);
      console.log('Model Emotion Loaded');

      // Warm up network
      MODEL_EMOTION.predict(tf.zeros([1, 64, 64, 1]));
      IS_MODEL_EMOTION_LOADED = true;
      // this.$bvToast.toast('Model Emotion Loaded.');
      this.tracking();
    },
    getEmotion(im, face_id) {
      console.log(im);
      const input = this.process_input(im);
      const result = this.predictEmotion(input);
      console.log(result);
      return result;
    },
    process_input(im) {
      const img = tf.browser.fromPixels(im, 1).toFloat();
      const offset = tf.scalar(255);
      const z1 = tf.scalar(0.5);
      const z2 = tf.scalar(2);
      const normalized = img.div(offset).sub(z1).mul(z2);
      const batched = normalized.reshape([1, 64, 64, 1]);

      return batched;
    },
    predictEmotion(input) {
      const startTime = performance.now();

      const r = MODEL_EMOTION.predict(input);
      const result = r.dataSync();
      const tresult = tf.tensor(result);
      const label_index = tf.argMax(tresult).dataSync()[0];

      const label_percent = result[label_index].toFixed(4) * 100;

      const totalTime = performance.now() - startTime;
      return { result, label: LABEL_EMOTIONS[label_index], percent: label_percent };
    },
    cropFace(rect, face_id) {
      console.log('STARTED');
      const img = document.getElementById('img');

      const { x } = rect;
      const { y } = rect;
      const w = rect.width;
      const h = rect.height;

      const ratio = img.naturalWidth / img.width;

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.id = face_id;
      canvas.className = 'canvas-face';
      canvas.width = 64;
      canvas.height = 64;
      ctx.drawImage(img, x * ratio, y * ratio, w * ratio, h * ratio, 0, 0, 64, 64);

      const canvas_color = document.createElement('canvas');
      const ctx_color = canvas_color.getContext('2d');
      canvas_color.id = `${face_id}_color`;
      canvas_color.className = 'canvas-face';
      canvas_color.width = 100;
      canvas_color.height = 100;
      ctx_color.drawImage(img, x * ratio, y * ratio, w * ratio, h * ratio, 0, 0, 80, 80);
      document.body.appendChild(canvas_color);


      // Convert Image to Greyscale
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const { data } = imageData;
      for (let i = 0; i < data.length; i += 4) {
        const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
        data[i] = avg; // red
        data[i + 1] = avg; // green
        data[i + 2] = avg; // blue
      }
      ctx.putImageData(imageData, 0, 0);
      document.body.appendChild(canvas);
    },
    clearFaceCanvas() {
      // $('#image-container .face-frame').remove();
      // $('.chart-result').remove();
      $('.canvas-face').remove();
    },

    generateResultChart(face_id, result_emotion) {
      var chart_emotion_id = `${face_id}_emotion_chart`;
      var chart_gender_id = `${face_id}_gender_chart`;
      var html = `
         <div class="col s12 m6 chart-result">
              <div class="card">
                <div class="card-content" style="text-align: center;">
                  <div class="chart-result-profile"><canvas id="${face_id}_profile_chart" width="100" height="100"></canvas></div>
                  <div>
                      <canvas id="${chart_emotion_id}"></canvas>
                  </div>
                </div>
              </div>
          </div>`;
      $('#card-item-container').append(html);

      var canvas_color = document.getElementById(`${face_id}_color`);
      var ctx_color = canvas_color.getContext('2d');
      var canvas_profile = document.getElementById(`${face_id}_profile_chart`);
      var ctx_profile = canvas_profile.getContext('2d');
      ctx_profile.drawImage(canvas_color, 0, 0);

      var options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
      };
      var chart_emotion = new Chart(document.getElementById(chart_emotion_id), {
        type: 'horizontalBar',
        data: {
          labels: [
            'Angry',
            'Disgust',
            'Fear',
            'Happy',
            'Sad',
            'Surprise',
            'Neutral',
          ],
          datasets: [
            {
              label: `Emotion: ${result_emotion.label}`,
              data: result_emotion.result,
              fill: false,
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)',
              ],
              borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)',
              ],
              borderWidth: 1,
            },
          ],
        },
        options,
      });
    },


  },
};
</script>

<style scoped>
@import "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css";
@import "https://cdnjs.cloudflare.com/ajax/libs/cropper/4.0.0/cropper.min.css";
@import "https://use.fontawesome.com/releases/v5.0.10/css/all.css";
@import "https://fontlibrary.org/face/cmu-sans-serif";
@import "https://fonts.googleapis.com/icon?family=Material+Icons";


.rects {
    border: 5px solid #a64ceb;
    left: -1000px;
    position: absolute;
    top: -1000px;
  }

  #img {
    position: absolute;
    top: 20%;
    left: 20%;
    width: 205px;
    height:205px;
  }

.demo-container {
  width: 50%;
  height: 330px;
  position: relative;
  background:#eee;
  overflow: hidden;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}

.dg.ac {
  z-index: 100 !important;
  top: 50px !important;
}
</style>
