from hittable import *
from texture import *
from material import *

class ConstantMedium(Hittable):
    def __init__(self, b: Hittable, d: float, a: Texture) -> None:
        self.boundary = b
        self.neg_inv_density = -1 / d
        self.phase_function = Isotropic(a)
        
    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        has_hit1, rec1 = self.boundary.hit(r, -math.inf, math.inf)
        if not has_hit1:
            return False, None
        
        has_hit2, rec2 = self.boundary.hit(r, rec1.t + 0.0001, math.inf)
        if not has_hit2:
            return False, None
        
        if rec1.t < t_min:
            rec1.t = t_min

        if rec2.t > t_max:
            rec2.t = t_max

        if rec1.t >= rec2.t:
            return False, None
        
        if rec1.t < 0:
            rec1.t = 0

        ray_length = r.d.len()
        dist_inside_boundary = (rec2.t - rec1.t) * ray_length
        hit_dist = self.neg_inv_density * math.log(random.random())

        if hit_dist > dist_inside_boundary:
            return False, None
        
        rec = HitRecord()
        rec.t = rec1.t + hit_dist / ray_length
        rec.p = r.at(rec.t)

        # Arbitrary since we're dealing with a volume.
        rec.normal = V3(1, 0, 0)
        rec.front_face = True

        rec.material = self.phase_function

        return True, rec

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return self.boundary.bounding_box(_time0, _time1)