from hittable import *
from material import *

class XYrect(Hittable):
    def __init__(self, _x0: float, _x1: float, _y0: float, _y1: float, _k: float, _mat: Material) -> None:
        self.x0 = _x0
        self.x1 = _x1
        self.y0 = _y0
        self.y1 = _y1
        self.k = _k
        self.mat = _mat

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        t = (self.k - r.o.z) / r.d.z
        if t < t_min or t > t_max:
            return False, None
        
        x = r.o.x + t * r.d.x
        y = r.o.y + t * r.d.y

        if x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1:
            return False, None
        
        rec = HitRecord()

        rec.t = t
        rec.p = r.at(t)
        outward_normal = V3(0, 0, 1)
        rec.set_face_normal(r, outward_normal)
        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (y - self.y0) / (self.y1 - self.y0)
        rec.material = self.mat

        return True, rec

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return True, AABB(V3(self.x0, self.y0, self.k - 0.0001), V3(self.x1, self.y1, self.k + 0.0001))
    
class XZrect(Hittable):
    def __init__(self, _x0: float, _x1: float, _z0: float, _z1: float, _k: float, _mat: Material) -> None:
        self.x0 = _x0
        self.x1 = _x1
        self.z0 = _z0
        self.z1 = _z1
        self.k = _k
        self.mat = _mat

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        t = (self.k - r.o.y) / r.d.y
        if t < t_min or t > t_max:
            return False, None
        
        x = r.o.x + t * r.d.x
        z = r.o.z + t * r.d.z

        if x < self.x0 or x > self.x1 or z < self.z0 or z > self.z1:
            return False, None
        
        rec = HitRecord()

        rec.t = t
        rec.p = r.at(t)
        outward_normal = V3(0, 1, 0)
        rec.set_face_normal(r, outward_normal)
        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.material = self.mat

        return True, rec

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return True, AABB(V3(self.x0, self.k - 0.0001, self.z0), V3(self.x1, self.k + 0.0001, self.z1))
    
class YZrect(Hittable):
    def __init__(self, _y0: float, _y1: float, _z0: float, _z1: float, _k: float, _mat: Material) -> None:
        self.y0 = _y0
        self.y1 = _y1
        self.z0 = _z0
        self.z1 = _z1
        self.k = _k
        self.mat = _mat

    def hit(self, r: Ray, t_min: float, t_may: float) -> tuple[bool, HitRecord]:
        t = (self.k - r.o.x) / r.d.x
        if t < t_min or t > t_may:
            return False, None
        
        y = r.o.y + t * r.d.y
        z = r.o.z + t * r.d.z

        if y < self.y0 or y > self.y1 or z < self.z0 or z > self.z1:
            return False, None
        
        rec = HitRecord()

        rec.t = t
        rec.p = r.at(t)
        outward_normal = V3(1, 0, 0)
        rec.set_face_normal(r, outward_normal)
        rec.u = (y - self.y0) / (self.y1 - self.y0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.material = self.mat

        return True, rec

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return True, AABB(V3(self.k - 0.0001, self.y0, self.z0), V3(self.k + 0.0001, self.y1, self.z1))