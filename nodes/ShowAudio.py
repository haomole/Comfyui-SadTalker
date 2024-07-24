import os
import torchaudio  # type: ignore
import folder_paths  # type: ignore


class ShowAudio:
    SUPPORTED_FORMATS = (".wav", ".mp3", ".ogg", ".flac", ".aiff", ".aif")

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if (
                os.path.isfile(os.path.join(input_dir, f))
                and f.endswith(ShowAudio.SUPPORTED_FORMATS)
            )
        ]
        return {"required": {"audio": (sorted(files), {"audio_upload": True})}}

    CATEGORY = "SadTalker"

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "load"

    def load(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)
        waveform, sample_rate = torchaudio.load(audio_path)
        audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (audio,)
