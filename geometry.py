import math

from vec import *
from ray import *
from hittable import *
from material import *

class Sphere(Hittable):
    def __init__(self, center: vec3, r: float, m: Material) -> None:
        self.center = center
        self.r = r
        self.m = m

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple:
        oc = vec_sub(r.o, self.center)

        a = vec_dot(r.d, r.d)
        half_b = vec_dot(oc, r.d)
        c = oc.len_sqr() - self.r * self.r
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return False, None

        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False, None

        rec = HitRecord()

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = vec_sdiv(vec_sub(rec.p, self.center), self.r)
        rec.set_face_normal(r, outward_normal)
        rec.material = self.m

        return True, rec
