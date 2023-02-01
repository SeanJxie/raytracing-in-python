import numpy as np

from vec import *
from ray import *

class camera:
    def __init__(self) -> None:
        self.aspect_ratio = 16.0 / 9.0

        self.viewport_ht = 2.0
        self.viewport_wt = self.aspect_ratio * self.viewport_ht
        self.focal_length = 1.0

        self.origin = vec3(0.0, 0.0, 0.0)
        self.horizontal = vec3(self.viewport_wt, 0, 0)
        self.vertical = vec3(0, self.viewport_ht, 0)

        self.half_horizontal = vec_sdiv(self.horizontal, 2)
        self.half_vertical = vec_sdiv(self.vertical, 2)
        self.lower_left_corner = vec_sub(vec_sub(vec_sub(self.origin, self.half_horizontal), self.half_vertical), vec3(0, 0, self.focal_length))

    def get_ray(self, u: float, v: float) -> ray:
        return ray(self.origin, vec_sub(vec_add(vec_add(self.lower_left_corner, vec_smul(self.horizontal, u)), vec_smul(self.vertical, v)), self.origin))

