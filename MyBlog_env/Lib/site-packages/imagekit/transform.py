params = {
    "height": "h",
    "width": "w",
    "quality": "q",
    "crop": "c",
    "crop_mode": "cm",
    "focus": "fo",
    "format": "f",
    "rounded_corner": "r",
    "border": "b",
    "rotation": "rt",
    "blur": "bl",
    "named": "n",
    "overlay_image": "oi",
    "overlay_x": "ox",
    "overlay_y": "oy",
    "overlay_focus": "ofo",
    "background": "bg",
    "progressive": "pr",
    "color_profile": "cp",
    "metadata": "md"
}

int_list = ["h", "w", "q", "r", "rt", "bl", "ox", "oy"]


class Transform(object):

    def __init__(self, raw):
        self.options = raw
        self.parsed = self.valid_transforms()

    def valid_transforms(self):
        _tparsed = []

        for data in self.options:
            _option = data
            _parsed = []
            for param, option in _option.items():
                for key, value in params.items():
                    if param in key:
                        code = params[param]
                        if code in int_list:
                            _parsed.append(code+"-"+str(int(option)))
                        else:
                            _parsed.append(code+"-"+str(option))

            transformation = ",".join(sorted(_parsed))
            _tparsed.append(transformation)

        return ':'.join(_tparsed)

