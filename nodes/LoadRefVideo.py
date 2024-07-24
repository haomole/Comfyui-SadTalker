import os
import folder_paths  # type: ignore
from moviepy.editor import VideoFileClip  # type: ignore

input_path = folder_paths.get_input_directory()


class LoadRefVideo:
    @classmethod
    def INPUT_TYPES(s):
        files = [
            f
            for f in os.listdir(input_path)
            if os.path.isfile(os.path.join(input_path, f))
            and f.split(".")[-1] in ["mp4", "webm", "mkv", "avi"]
        ]
        return {
            "required": {
                "video": (files,),
            }
        }

    CATEGORY = "SadTalker"
    RETURN_TYPES = ("VIDEO", "VIDEOSTRING")
    RETURN_NAMES = ("video", "video_path")
    OUTPUT_NODE = False
    FUNCTION = "load_video"

    def load_video(self, video):
        video_path = os.path.join(input_path, video)
        video_clip = VideoFileClip(video_path)
        return (
            video_clip,
            video_path,
        )
