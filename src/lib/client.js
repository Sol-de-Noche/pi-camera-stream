import axios from "axios";

class Client {
  constructor(domain) {
    axios.defaults.baseURL = domain;
    console.debug("Host:", domain);
  }

  async status() {
    try {
      var response = await axios.get("/api/status");
      if (response.status == 200) {
        return response.data;
      }
    } catch (err) {
      console.log(err);
    }
    return {};
  }

  async record() {
    try {
      var data = { status: true };
      var response = await axios.post("/api/status", data);
      if (response.status == 200) {
        return response.data;
      }
    } catch (err) {
      console.log(err);
    }
    return {};
  }

  async stop() {
    try {
      var data = { status: false };
      var response = await axios.post("/api/status", data);
      if (response.status == 200) {
        return response.data;
      }
    } catch (err) {
      console.log(err);
    }
    return {};
  }

  async getImages() {
    try {
      var response = await axios.get("/api/images");
      if (response.status == 200) {
        return response.data.images;
      }
    } catch (err) {
      console.log(err);
    }
    return {};
  }
  async getVideos() {
    try {
      var response = await axios.get("/api/videos");
      if (response.status == 200) {
        return response.data.videos;
      }
    } catch (err) {
      console.log(err);
    }
    return {};
  }
}

export default Client;
