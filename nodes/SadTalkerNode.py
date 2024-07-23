import logging
import os
import shutil
import torch  # type: ignore
import numpy as np  # type: ignore
from PIL import Image  # type: ignore
import soundfile as sf  # type: ignore
from datetime import datetime


from ..SadTalker.src.Pb import SadTalker


class SadTalkerNode:

    def __init__(self):
        self.checkpoint_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "SadTalker", "checkpoints")
        )
        self.config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "SadTalker", "src", "config")
        )
        self.output_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "SadTalker", "output")
        )
        self.comfy_output_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "output")
        )
        self.input_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "SadTalker", "input")
        )
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.comfy_output_dir, exist_ok=True)

        # 实例化 SadTalker
        self.sad_talker = SadTalker(
            checkpoint_path=self.checkpoint_path,
            config_path=self.config_path,
            lazy_load=True,
        )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "audio": ("AUDIO",),
                "poseStyle": ("INT", {"default": 0, "min": 0, "max": 46}),
                "faceModelResolution": (["256", "512"], {"default": "256"}),
                "preprocess": (
                    ["crop", "resize", "full", "extcrop", "extfull"],
                    {"default": "crop"},
                ),
                "stillMode": (["true", "false"], {"default": "false"}),
                "batchSizeInGeneration": (
                    "INT",
                    {"default": 2, "min": 0, "max": 10},
                ),
                "gfpganAsFaceEnhancer": (
                    ["true", "false"],
                    {"default": "false"},
                ),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "video_path",
        "show_video_path",
    )
    FUNCTION = "generate"
    CATEGORY = "SadTalker"

    def generate(
        self,
        image,
        audio,
        poseStyle,
        faceModelResolution,
        preprocess,
        stillMode,
        batchSizeInGeneration,
        gfpganAsFaceEnhancer,
    ):

        stillMode = stillMode == "true"
        gfpganAsFaceEnhancer = gfpganAsFaceEnhancer == "true"

        # 生成时间戳目录
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        input_dir = os.path.join(self.input_dir, timestamp)
        os.makedirs(input_dir, exist_ok=True)

        # 保存图像
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()
        if image.ndim == 4:
            image = image[0]
        if image.ndim == 3:
            if image.shape[2] in {1, 3}:
                if image.shape[2] == 1:
                    image = np.squeeze(image, axis=2)
            else:
                raise ValueError("Unexpected number of channels in image tensor")

        image = (image * 255).astype(np.uint8)
        image_path = os.path.join(input_dir, "input_image.png")
        Image.fromarray(image).save(image_path)

        # 提取并保存音频
        waveform = audio["waveform"].cpu().numpy().squeeze()
        sample_rate = audio["sample_rate"]
        if waveform.ndim == 2:
            waveform = waveform.T
        audio_path = os.path.join(input_dir, "input_audio.wav")
        sf.write(audio_path, waveform, sample_rate)

        result = self.sad_talker.test(
            source_image=image_path,
            driven_audio=audio_path,
            preprocess=preprocess,
            still_mode=stillMode,
            use_enhancer=gfpganAsFaceEnhancer,
            batch_size=batchSizeInGeneration,
            size=int(faceModelResolution),
            pose_style=poseStyle,
            exp_scale=1.0,
            use_ref_video=False,
            ref_video=None,
            ref_info=None,
            use_idle_mode=False,
            length_of_audio=0,
            use_blink=True,
            result_dir=self.output_dir,
        )

        comy_out = os.path.join(self.comfy_output_dir, timestamp + ".mp4")
        shutil.copy(result, comy_out)

        return (
            result,
            comy_out,
        )
