class ShowVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "show_video_path": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    OUTPUT_NODE = True
    INPUT_IS_LIST = True
    RETURN_TYPES = ()
    OUTPUT_IS_LIST = (True,)

    FUNCTION = "generate"
    CATEGORY = "SadTalker"

    def generate(self, show_video_path, unique_id=None, extra_pnginfo=None):
        if unique_id and extra_pnginfo and "workflow" in extra_pnginfo[0]:
            workflow = extra_pnginfo[0]["workflow"]
            node = next(
                (x for x in workflow["nodes"] if str(x["id"]) == unique_id[0]), None
            )
            if node:
                node["widgets_values"] = [show_video_path]

        # 返回视频路径
        return {
            "ui": {"show_video_path": show_video_path},
            "result": (show_video_path,),
        }
