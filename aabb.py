from vec import *
from ray import *

class AABB:
    def __init__(self, mini: V3, maxi: V3) -> None:
        self.mini = mini
        self.maxi = maxi

    def hit(self, r: Ray, t_min: float, t_max: float) -> bool:
        for a in range(3):
            invd = 1.0 / r.d[a]
            t0 = (self.mini[a] - r.o[a]) * invd
            t1 = (self.maxi[a] - r.o[a]) * invd

            if invd < 0.0:
                t0, t1 = t1, t0

            if t0 > t_min:
                t_min = t0

            if t1 < t_max:
                t_max = t1

            if t_max <= t_min:
                return False
        
        return True
    

def surrounding_box(box0: AABB, box1: AABB) -> AABB:
    small = V3(
        min(box0.mini.x, box1.mini.x),
        min(box0.mini.y, box1.mini.y),
        min(box0.mini.z, box1.mini.z)
    )

    big = V3(
        max(box0.maxi.x, box1.maxi.x),
        max(box0.maxi.y, box1.maxi.y),
        max(box0.maxi.z, box1.maxi.z)
    )

    return AABB(small, big)