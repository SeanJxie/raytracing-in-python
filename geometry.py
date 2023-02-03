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

    def hit(self, r: ray, t_min: float, t_max: float) -> tuple:
        oc = vec_sub(r.origin(), self.center)

        a = vec_dot(r.direction(), r.direction())
        half_b = vec_dot(oc, r.direction())
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

        rec = hit_record()

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = vec_sdiv(vec_sub(rec.p, self.center), self.r)
        rec.set_face_normal(r, outward_normal)
        rec.material = self.m

        return True, rec

# class triangle(hittable):
#     def __init__(self, v0: vec3, v1: vec3, v2: vec3, m: material) -> None:
#         self.v0 = v0
#         self.v1 = v1
#         self.v2 = v2
#         self.m = m

#     def hit(self, r: ray, t_min: float, t_max: float) -> tuple:
#         #  Möller–Trumbore ray-triangle intersection algorithm
#         epsilon = 0.0000001
#         v0 = self.v0
#         v1 = self.v1
#         v2 = self.v2

#         edge1 = vec_sub(v1, v0)
#         edge2 = vec_sub(v2, v0)

#         h = vec_cross(r.direction(), edge2)
#         a = vec_dot(edge1, h)

#         if a > -epsilon and a < epsilon:
#             return False, None # Ray parralel to triangle

#         f = 1 / a
#         s = vec_sub(r.origin(), v0)
#         u = f * vec_dot(s, h)

#         if u < 0.0 or u > 1.0:
#             return False, None

#         q = vec_cross(s, edge1)
#         v = f * vec_dot(r.direction(), q)
        
#         if v < 0.0 or u + v > 1.0:
#             return False, None
        
#         t = f * vec_dot(edge2, q)
#         rec = hit_record()
#         if t > epsilon and t_min <= t <= t_max:

#             # Update hit record
#             rec.t = t
#             rec.p = r.at(rec.t)
        
#             outward_normal = vec3(
#                 edge1.y() * edge2.z() - edge1.z() * edge2.y(), 
#                 edge1.z() * edge2.x() - edge1.x() * edge2.z(), 
#                 edge1.x() * edge2.y() - edge1.y() * edge2.x(), 
#             )

#             rec.set_face_normal(r, outward_normal)
#             rec.material = self.m

#             return True, rec
#         else:
#             return False, None
    
        