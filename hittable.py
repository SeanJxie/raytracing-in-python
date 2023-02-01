import numpy as np

from vec import *
from ray import *

class hit_record:
    def __init__(self) -> None:
        self.p = None
        self.normal = None
        self.material = None
        self.t = None
        self.front_face = None

    def set_face_normal(self, r: ray, outward_normal: vec3) -> None:
        self.front_face = vec_dot(r.direction(), outward_normal) < 0
        
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = outward_normal.neg()

class hittable:
    def __init__(self) -> None:
        pass

    def hit(self, r: ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        print(rec.__dict__)

        pass
