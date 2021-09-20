<template>
  <div class="container">
    <div class="card">
      <div class="card">
        <div class="card-content">
          <div class="content">
            <img
              class="camera-bg"
              style="background-attachment: fixed"
              id="bg"
              :src="videoUrl"
            />
          </div>
          <div class="card">
            <footer class="card-footer">
              <div class="card-footer-item">
                <div class="buttons has-addons is-centered">
                  <button :class="'button ' + videoClass" @click="toggleVideo">
                    <span class="icon is-small"
                      ><i :class="videoIcon"></i
                    ></span>
                  </button>
                </div>
              </div>
              <div class="card-footer-item">
                <div class="buttons has-addons is-centered">
                  <button
                    :disabled="!recording"
                    class="button is-danger"
                    @click="stop"
                  >
                    <span class="icon is-small"
                      ><i class="fas fa-pause"></i
                    ></span></button
                  ><button
                    :disabled="recording"
                    class="button is-primary"
                    @click="record"
                  >
                    <span class="icon is-small"
                      ><i class="fas fa-camera"></i
                    ></span>
                  </button>
                </div>
              </div>
              <div class="card-footer-item">
                <div class="buttons has-addons is-centered">
                  <button class="button" @click="loadImages">
                    <span class="icon is-small"
                      ><i :class="loadingClass"></i></span
                    ><span>Reload</span>
                  </button>
                </div>
              </div>
            </footer>
          </div>
        </div>
      </div>
    </div>
    <div class="box">
      <div class="tabs is-boxed">
        <ul>
          <li :class="imagesClass">
            <a @click="toggleImages">
              <span class="icon is-small"
                ><i class="fas fa-image" aria-hidden="true"></i
              ></span>
              <span>Pictures</span>
            </a>
          </li>
          <li :class="videosClass">
            <a @click="toggleVideos">
              <span class="icon is-small"
                ><i class="fas fa-film" aria-hidden="true"></i
              ></span>
              <span>Videos</span>
            </a>
          </li>
        </ul>
      </div>
      <div :class="'columns is-multiline ' + displayImages">
        <div
          class="column is-one-fifth"
          v-for="(image, index) in images"
          :key="index"
        >
          <figure class="image">
            <img :src="domain + image" :title="image" />
          </figure>
        </div>
      </div>
      <div :class="'columns is-multiline ' + displayVideos">
        <div
          class="column is-one-fifth"
          v-for="(video, index) in videos"
          :key="index"
        >
          <figure class="omage">
            <video controls width="250" :src="domain + video">
              Sorry, your browser doesn't support embedded videos.
            </video>
            <a :href="domain + video" :download="cleanName(video)">Download</a>
          </figure>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Client from "./lib/client.js";

export default {
  name: "App",
  data() {
    return {
      domain: location.href,
      client: null,
      playing: false,
      recording: false,
      loading: false,
      showImages: true,
      showVideos: false,
      images: [],
      videos: [],
    };
  },
  computed: {
    videoUrl() {
      return this.playing
        ? this.domain + "video_feed"
        : "img/logosoldenoite.png";
    },
    videoClass() {
      return this.playing ? "is-danger" : "is-primary";
    },
    videoIcon() {
      return this.playing ? "fas fa-video-slash" : "fas fa-video";
    },
    loadingClass() {
      return this.loading ? "fas fa-sync fa-spin" : "fas fa-sync";
    },
    imagesClass() {
      return this.showImages ? "is-active" : "";
    },
    videosClass() {
      return this.showVideos ? "is-active" : "";
    },
    displayImages() {
      return !this.showImages ? "is-hidden" : "";
    },
    displayVideos() {
      return !this.showVideos ? "is-hidden" : "";
    },
  },
  mounted() {
    if (this.$root.debug) {
      this.domain = "http://localhost:8000/";
    }
    this.client = new Client(this.domain);
    this.status();
    this.loadImages();
  },
  timers: {
    loadImages: { time: 1000 * 60, autostart: true, repeat: true },
  },
  methods: {
    cleanName(name) {
      name = name.replace("videos/", "");
      name = name.replace(".mp4", "");
      return name;
    },
    toggleVideo() {
      console.log("Toggling video");
      this.playing = !this.playing;
    },
    toggleImages() {
      this.showImages = true;
      this.showVideos = false;
    },
    toggleVideos() {
      this.showVideos = true;
      this.showImages = false;
    },
    async status() {
      this.recording = await this.client.status();
    },
    async record() {
      this.recording = await this.client.record();
    },
    async stop() {
      this.recording = await this.client.stop();
    },
    async loadImages() {
      console.log("Loading images...");
      this.loading = true;
      await new Promise((r) => setTimeout(r, 2000));

      this.images = await this.client.getImages();
      this.images.sort();

      await new Promise((r) => setTimeout(r, 2000));

      this.videos = await this.client.getVideos();
      this.videos.sort();

      await new Promise((r) => setTimeout(r, 2000));
      this.loading = false;
    },
  },
};
</script>
<style lang="scss">
@import "~bulma/sass/utilities/_all";
@import "~bulma/sass/base/_all";

@import "~bulma/sass/elements/_all";
@import "~bulma/sass/form/_all";
@import "~bulma/sass/components/_all";
@import "~bulma/sass/grid/_all";
@import "~bulma/sass/helpers/_all";
@import "~bulma/sass/layout/_all";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.camera-bg {
  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 640;
}
</style>
