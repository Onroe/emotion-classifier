<!-- View to capture face from webcam -->
<template>
      <div>
          <video autoplay playsinline muted id="compwebcam" width="300" height="300"></video>
      </div>
</template>

<script>
// javascript library for webcam
import { Webcam } from '../assets/webcam';

export default {
  name: 'WebCam',
  data() {
    return {
      webcam: null,
    };
  },
  mounted() {
    this.loadWebcam();
  },
  methods: {
    loadWebcam() {
      this.webcam = new Webcam(document.getElementById('compwebcam'));
      this.webcam.setup();
    },
  },
};
</script>
