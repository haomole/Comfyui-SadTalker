import logging
import os, sys

SadTalkerPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "SadTalker"))
sys.path.append(SadTalkerPath)

from .nodes.ShowText import ShowText
from .nodes.ShowVideo import ShowVideo
from .nodes.ShowAudio import ShowAudio
from .nodes.SadTalkerNode import SadTalkerNode

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "SadTalker": SadTalkerNode,
    "ShowVideo": ShowVideo,
    "ShowText": ShowText,
    "ShowAudio": ShowAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SadTalker": "🦚 SadTalker",
    "ShowVideo": "🎥 Show Video",
    "ShowText": "💬 Show Text",
    "ShowAudio": "🔊 Show Audio",
}


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
