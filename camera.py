import math

from vec import *
from ray import *

class camera:
    def __init__(self, lookfrom: vec3, lookat: vec3, vup: vec3, vfov: float, aspect_ratio: float, aperture: float, 
            focus_dist: float) -> None:

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

    def get_ray(self, s: float, t: float) -> ray:
        rd = vec_smul(random_in_unit_disk(), self.lens_radius)
        offset = vec_add(vec_smul(self.u, rd.x()), vec_smul(self.v, rd.y()))

        return ray(vec_add(self.origin, offset), 
            vec_sub(vec_sub(vec_add(vec_add(self.lower_left_corner, vec_smul(self.horizontal, s)), 
            vec_smul(self.vertical, t)), self.origin), offset))

