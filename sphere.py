import math

import numpy as np

from vec import *
from ray import *
from hittable import *
from material import *

class sphere(hittable):
    def __init__(self, center: vec3, r: float, m: material) -> None:
        self.center = center
        self.r = r
        self.m = m

    def hit(self, r: ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        oc = vec_sub(r.origin(), self.center)

        a = vec_dot(r.direction(), r.direction())
        half_b = vec_dot(oc, r.direction())
        c = oc.len_sqr() - self.r * self.r
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = vec_sdiv(vec_sub(rec.p, self.center), self.r)
        rec.set_face_normal(r, outward_normal)
        rec.material = self.m

        return True


