from vec import *
from ray import *
from aabb import *

class HitRecord:
    def __init__(self) -> None:
        self.p = None
        self.normal = None
        self.material = None
        self.t: float = 0
        self.u: float = 0
        self.v: float = 0
        self.front_face: bool = False

    def set_face_normal(self, r: Ray, outward_normal: V3) -> None:
        self.front_face = vec_dot(r.d, outward_normal) < 0
        
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = outward_normal.neg()

class Hittable:
    def __init__(self) -> None:
        pass

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        pass

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        pass

class Translate(Hittable):
    def __init__(self, h: Hittable, displacement: V3) -> None:
        self.h = h
        self.offset = displacement

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        moved_r = Ray(vec_sub(r.o, self.offset), r.d, r.time)
        has_hit, rec = self.h.hit(moved_r, t_min, t_max)
        if not has_hit:
            return False, None

        rec.p = vec_add(rec.p, self.offset)
        rec.set_face_normal(moved_r, rec.normal)

        return True, rec

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        b, output_box = self.h.bounding_box(_time0, _time1)
        if not b:
            return False

        return True, AABB(
            vec_add(output_box.mini, self.offset),
            vec_add(output_box.maxi, self.offset),
        )

# BUG Rotation is absolutely in shambles        
class RotateY(Hittable):
    def __init__(self, h: Hittable, angle: float) -> None:
        radians = math.radians(angle)
        self.sin_theta = math.sin(radians)
        self.cos_theta = math.cos(radians)
        self.h = h
        self.hasbox, self.bbox = self.h.bounding_box(0, 1)

        minvec = V3(math.inf, math.inf, math.inf)
        maxvec = V3(-math.inf, -math.inf, -math.inf)

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    x = i*self.bbox.maxi.x + (1-i)*self.bbox.mini.x
                    y = j*self.bbox.maxi.y + (1-j)*self.bbox.mini.y
                    z = k*self.bbox.maxi.z + (1-k)*self.bbox.mini.z

                    newx =  self.cos_theta*x + self.sin_theta*z;
                    newz = -self.sin_theta*x + self.cos_theta*z;
    
                    tester = V3(newx, y, newz)

                    minvec.x = min(minvec.x, tester.x)
                    maxvec.x = max(maxvec.x, tester.x)

                    minvec.y = min(minvec.y, tester.y)
                    maxvec.y = max(maxvec.y, tester.y)

                    minvec.z = min(minvec.z, tester.z)
                    maxvec.z = max(maxvec.z, tester.z)

        self.bbox = AABB(minvec, maxvec)

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        origin = r.o
        direction = r.d

        origin.x = self.cos_theta * r.o.x - self.sin_theta * r.o.z
        origin.z = self.sin_theta * r.o.x + self.cos_theta * r.o.z

        direction.x = self.cos_theta * r.d.x - self.sin_theta * r.d.z
        direction.z = self.sin_theta * r.d.x + self.cos_theta * r.d.z

        rotated_r = Ray(origin, direction, r.time)
        has_hit, rec = self.h.hit(rotated_r, t_min, t_max)
        if not has_hit:
            return False, None
        
        p = rec.p
        normal = rec.normal

        p.x = self.cos_theta * rec.p.x + self.sin_theta * rec.p.z
        p.z = -self.sin_theta * rec.p.x + self.cos_theta * rec.p.z

        normal.x = self.cos_theta * rec.normal.x + self.sin_theta * rec.normal.z
        normal.z = -self.sin_theta * rec.normal.x + self.cos_theta * rec.normal.z

        rec.p = p
        rec.set_face_normal(rotated_r, normal)

        return True, rec

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return self.has_box, self.bbox