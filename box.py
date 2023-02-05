from vec import *
from hittable import *
from hittablelist import *
from material import *
from aarect import *

class Box(Hittable):
    def __init__(self, p0: V3, p1: V3, mat: Material) -> None:
        self.box_min = p0
        self.box_max = p1

        self.sides = HittableList()

        self.sides.add(XYrect(p0.x, p1.x, p0.y, p1.y, p1.z, mat))
        self.sides.add(XYrect(p0.x, p1.x, p0.y, p1.y, p0.z, mat))

        self.sides.add(XZrect(p0.x, p1.x, p0.z, p1.z, p1.y, mat))
        self.sides.add(XZrect(p0.x, p1.x, p0.z, p1.z, p0.y, mat))

        self.sides.add(YZrect(p0.y, p1.y, p0.z, p1.z, p1.x, mat))
        self.sides.add(YZrect(p0.y, p1.y, p0.z, p1.z, p0.x, mat))

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        return self.sides.hit(r, t_min, t_max)

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return True, AABB(self.box_min, self.box_max)
    
