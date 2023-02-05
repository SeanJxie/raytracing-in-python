from hittable import *
from texture import *
from material import *

class ConstantMedium(Hittable):
    def __init__(self, b: Hittable, d: float, a: Texture) -> None:
        self.boundary = b
        self.neg_inv_density = -1 / d
        self.phase_function = Isotropic(a)
        
    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        pass

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return self.boundary.bounding_box(_time0, _time1)