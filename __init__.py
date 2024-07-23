import logging
import os, sys

SadTalkerPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "SadTalker"))
sys.path.append(SadTalkerPath)

from .nodes.ShowText import ShowText
from .nodes.ShowVideo import ShowVideo
from .nodes.SadTalkerNode import SadTalkerNode

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "SadTalker": SadTalkerNode,
    "ShowVideo": ShowVideo,
    "ShowText": ShowText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SadTalker": "🦚SadTalker",
    "ShowVideo": "🎥Show Video",
    "ShowText": "💬Show Text",
}


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
