import shutil
import uuid
import os
import cv2
import logging


project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
)
output_directory = os.path.join(project_root, "output")


def load_video_to_cv2(input_path):
    video_stream = cv2.VideoCapture(input_path)
    fps = video_stream.get(cv2.CAP_PROP_FPS)
    full_frames = []
    while True:
        still_reading, frame = video_stream.read()
        if not still_reading:
            video_stream.release()
            break
        full_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return full_frames, fps


def save_video_with_watermark(video, audio, save_path, watermark=False, target_fps=30):
    temp_video = os.path.join(output_directory, str(uuid.uuid4()) + "_video.mp4")

    cmd = (r'ffmpeg -y -hide_banner -loglevel error -i "%s" -r %d -qscale 0 "%s"') % (
        video,
        target_fps,
        temp_video,
    )
    os.system(cmd)

    temp_file = os.path.join(output_directory, str(uuid.uuid4()) + ".mp4")
    cmd = (
        r'ffmpeg -i "%s" -i "%s" '
        r"-c:v libx264 -b:v 5000k -maxrate 5000k -bufsize 10000k "
        r'-c:a aac -b:a 122k -ac 2 -ar 44100 -strict experimental "%s" '
    ) % (temp_video, audio, temp_file)

    os.system(cmd)

    try:
        if not watermark:
            # 如果不需要水印，直接将临时文件移动到保存路径
            shutil.copy(temp_file, save_path)
        else:
            # 获取水印图片路径
            dir_path = os.path.dirname(os.path.realpath(__file__))
            watermark_path = os.path.join(dir_path, "../../docs/sadtalker_logo.png")

            # 构建 FFmpeg 命令以添加水印
            cmd = [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                temp_file,
                "-i",
                watermark_path,
                "-filter_complex",
                "[1]scale=100:-1[wm];[0][wm]overlay=(main_w-overlay_w)-10:10",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-ar",
                "16000",
                "-shortest",
                save_path,
            ]

            os.system(cmd)
    except Exception as e:
        logging.error("Error:", e)

    # 确保临时视频文件被删除
    if os.path.exists(temp_video):
        os.remove(temp_video)
    if os.path.exists(temp_file):
        os.remove(temp_file)
