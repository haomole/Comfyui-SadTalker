import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

let video;

const ext = {
  name: "SadTalker.ShowVideo",

  async beforeRegisterNodeDef (nodeType, nodeData, app) {
    if (nodeData.name === "ShowVideo") {
      function populate (videoPath) {

        const filePath = videoPath[0]
        if (video && filePath) {
          const fileName = filePath.split('\\').pop();
          video.src = api.apiURL(`/view?filename=${fileName}`);
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
      if (video) return;
      const container = document.createElement("div");
      container.style.background = "rgba(0,0,0,0.25)";
      container.style.textAlign = "center";
      video = document.createElement("video")
      video.style.height = video.style.width = "100%";
      video.controls = true
      video.classList.add("comfy-video")
      video.setAttribute("name", "media")
      container.replaceChildren(video);
      node.addDOMWidget("video", "VIDEO", container)
    }
  }
};



app.registerExtension(ext);
