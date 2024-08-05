# Comfyui-SadTalker

### 版权声明（Copyright）

- [SadTalker](https://github.com/OpenTalker/SadTalker)

### 注意（Notice）

- 首次开发插件，节点可能存在问题，如果遇到了困难，请提交 Issues.（This is the first time to develop a plugin. There may be problems with the node. If you run into difficulties, please submit Issues.）

### 例子（Examples）

![Workflow](./examples/workflow.png)

### 可能遇到的问题(Problems That You May Have)

- 如果报错 audio 不存在或者未定义，请升级 comfyui.(If you get the error that audio does not exist or is undefined, upgrade comfyui.)
- 如果 video 显示异常，请刷新浏览器.（Reload your browser if the video displays abnormally.）
- 如果报错：FileNotFoundError: [Errno 2] No such file or directory: 'F:\\\\ComfyUI-aki-v1.3\\output\\6b5735c4-ef50-4933-a34d-ccbad3b5936d.mp4'，请下载ffmpeg并且将ffmpeg/bin目录加入环境变量中.（If you get an error: FileNotFoundError: [Errno 2] No such file or directory: 'F:\\\\ComfyUI-aki-v1.3\\output\\6b5735c4-ef50-4933-a34d-ccbad3b5936d.mp4', download ffmpeg and add the ffmpeg/bin directory to the environment variable.）

### 安装（Install）

1. ...custom_nodes\Comfyui-SadTalker\SadTalker\checkpoints\
   - SadTalker_V0.0.2_256.safetensors（691MB）
   - SadTalker_V0.0.2_512.safetensors（691MB）
   - mapping_00109-model.pth.tar（148MB）
   - mapping_00229-model.pth.tar（148MB）
2. ...(comfyui root)\gfpgan\weights\
   - alignment_WFLW_4HG.pth（184MB）
   - detection_Resnet50_Final.pth（104MB）
   - GFPGANv1.4.pth（332MB）
   - parsing_parsenet.pth（81.3MB）

### 联系我（Contact Me）

<image src='./examples/qq.jpg' style="width:30%;"></image>
