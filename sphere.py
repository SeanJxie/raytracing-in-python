from math import sqrt

from vec import *
from ray import *
from hittable import *
from material import *
from aabb import *

class Sphere(Hittable):
    def __init__(self, c: V3, r: float, m: Material) -> None:
        self.c = c
        self.r = r
        self.m = m

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        oc = vec_sub(r.o, self.c)

        a = vec_dot(r.d, r.d)
        half_b = vec_dot(oc, r.d)
        c = oc.len_sqr() - self.r * self.r
        d = half_b * half_b - a * c

        if d < 0:
            return False, None

        sqrtd = sqrt(d)

        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False, None

        rec = HitRecord()

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = vec_sdiv(vec_sub(rec.p, self.c), self.r)
        rec.set_face_normal(r, outward_normal)
        rec.u, rec.v = self.get_sphere_uv(outward_normal)
        rec.material = self.m

        return True, rec
    
    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        out = AABB(
            vec_sub(self.c, V3(self.r, self.r, self.r)),
            vec_add(self.c, V3(self.r, self.r, self.r))
        )

        return True, out

    def get_sphere_uv(self, p: V3) -> tuple[float, float]:
        theta = math.acos(-p.y)
        phi = math.atan2(-p.z, p.x) + math.pi

        u = phi / (2 * math.pi)
        v = theta / math.pi

        return u, v

class MovingSphere(Hittable):
    def __init__(self, c0: V3, c1: V3, _t0: float, _t1: float, r: float, m: Material) -> None:
        self.c0 = c0
        self.c1 = c1
        self.t0 = _t0
        self.t1 = _t1
        self.r = r
        self.m = m

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        oc = vec_sub(r.o, self.center(r.time))

        a = vec_dot(r.d, r.d)
        half_b = vec_dot(oc, r.d)
        c = oc.len_sqr() - self.r * self.r
        d = half_b * half_b - a * c

        if d < 0:
            return False, None

        sqrtd = sqrt(d)

        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False, None

        rec = HitRecord()

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = vec_sdiv(vec_sub(rec.p, self.center(r.time)), self.r)
        rec.set_face_normal(r, outward_normal)
        rec.material = self.m

        return True, rec

    def center(self, time: float) -> V3:
        return vec_add(self.c0, vec_smul(vec_sub(self.c1, self.c0), (time - self.t0) / (self.t1 - self.t0)))
    
    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        box0 = AABB(
            vec_sub(self.center(_time0), V3(self.r, self.r, self.r)),
            vec_add(self.center(_time0), V3(self.r, self.r, self.r))
        )
        box1 = AABB(
            vec_sub(self.center(_time1), V3(self.r, self.r, self.r)),
            vec_add(self.center(_time1), V3(self.r, self.r, self.r))
        )

        return True, surrounding_box(box0, box1)