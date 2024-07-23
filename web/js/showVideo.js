import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

let video;

const ext = {
  name: "SadTalker.ShowVideo",

  async beforeRegisterNodeDef (nodeType, nodeData, app) {
    if (nodeData.name === "ShowVideo") {
      function populate (videoPath) {
        // // 清理旧的视频控件
        // if (this.widgets) {
        //   for (let i = 1; i < this.widgets.length; i++) {
        //     this.widgets[i].onRemove?.();
        //   }
        //   this.widgets.length = 1;
        // }

        const isOutputNode = nodeData.output_node
        const filePath = videoPath[0]
        if (video && filePath) {
          const host = `http://${window.location.hostname}:${window.location.port}`;
          const fileName = filePath.split('\\').pop();
          console.log(`${host}/view?filename=${fileName}`);
          video.src = `${host}/view?filename=${fileName}`
          console.log(video);
          video.play();
        }
      }

      // When the node is executed we will be sent the input video path, display this in the widget
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        populate.call(this, message.show_video_path);
      };

      const onConfigure = nodeType.prototype.onConfigure;
      nodeType.prototype.onConfigure = function () {
        onConfigure?.apply(this, arguments);
        if (this.widgets_values?.length) {
          populate.call(this, this.widgets_values);
        }
      };
    }
  },

  loadedGraphNode (node, app) {
    if (node.type == "ShowVideo") {
      console.log('loadedGraphNode-loadedGraphNode');
      if (video) return;
      const container = document.createElement("div");
      container.style.background = "rgba(0,0,0,0.25)";
      container.style.textAlign = "center";
      video = document.createElement("video")
      video.style.height = video.style.width = "100%";
      video.controls = true
      video.classList.add("comfy-video")
      video.setAttribute("name", "media")
      // video.src = "http://127.0.0.1:8189/view?filename=20240723170624.mp4"
      container.replaceChildren(video);
      node.addDOMWidget("video", "VIDEO", container)
    }
  }
};



app.registerExtension(ext);
