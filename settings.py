from vec import *

class Settings:
    def __init__(self, image_wt: float, image_ht: float, bg_col: V3, samples: int, max_trace_depth: int) -> None:
        self.wt = image_wt
        self.ht = image_ht
        self.bg_col = bg_col
        self.samples = samples
        self.max_depth = max_trace_depth

        self.aspect_ratio = self.wt / self.ht


