import math

from vec import *
from ray import *

class Camera:
    def __init__(self, lookfrom: V3, lookat: V3, vup: V3, vfov: float, aspect_ratio: float, aperture: float, 
            focus_dist: float, _time0: float, _time1: float) -> None:

        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        viewport_ht = 2.0 * h
        viewport_wt = aspect_ratio * viewport_ht

        self.w = vec_unit(vec_sub(lookfrom, lookat))
        self.u = vec_unit(vec_cross(vup, self.w))
        self.v = vec_cross(self.w, self.u)

        self.origin = lookfrom
        self.horizontal = vec_smul(self.u, viewport_wt * focus_dist)
        self.vertical = vec_smul(self.v, viewport_ht * focus_dist)

        # Temporary halfs
        half_horizontal = vec_sdiv(self.horizontal, 2)
        half_vertical = vec_sdiv(self.vertical, 2)

        self.lower_left_corner = vec_sub(vec_sub(vec_sub(self.origin, half_horizontal), half_vertical), 
            vec_smul(self.w, focus_dist))

        self.lens_radius = aperture / 2
        self.time0 = _time0 # Shutter open
        self.time1 = _time1 # Shutter close

    def get_ray(self, s: float, t: float) -> Ray:
        rd = vec_smul(vec_rand_in_unit_disk(), self.lens_radius)
        offset = vec_add(vec_smul(self.u, rd.x), vec_smul(self.v, rd.y))

        return Ray(
            vec_add(self.origin, offset), vec_sub(vec_sub(vec_add(vec_add(self.lower_left_corner, vec_smul(self.horizontal, s)), 
            vec_smul(self.vertical, t)), self.origin), offset),
            random.uniform(self.time0, self.time1)
        )

