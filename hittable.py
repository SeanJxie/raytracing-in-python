from vec import *
from ray import *

class HitRecord:
    def __init__(self) -> None:
        self.p = None
        self.normal = None
        self.material = None
        self.t = None
        self.front_face = None

    def set_face_normal(self, r: Ray, outward_normal: vec3) -> None:
        self.front_face = vec_dot(r.d, outward_normal) < 0
        
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = outward_normal.neg()

class Hittable:
    def __init__(self) -> None:
        pass

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple:
        pass
