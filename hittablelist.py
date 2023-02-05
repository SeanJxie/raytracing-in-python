from functools import cmp_to_key

from hittable import *

class HittableList(Hittable):
    def __init__(self) -> None:
        self.objects = []

    def sort(self, cmp: 'function') -> None:
        self.objects = sorted(self.objects, key=cmp_to_key(cmp))

    def clear(self) -> None:
        self.objects.clear()

    def add(self, obj: Hittable) -> None:
        self.objects.append(obj)

    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max

        for obj in self.objects:
            has_hit, temp_rec = obj.hit(r, t_min, closest_so_far)
            if has_hit:
                hit_anything = True
                closest_so_far = temp_rec.t

                # Set rec to temp rec
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.t = temp_rec.t
                rec.u = temp_rec.u
                rec.v = temp_rec.v
                rec.front_face = temp_rec.front_face
                rec.material = temp_rec.material

        return hit_anything, rec

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        if len(self.objects) == 0:
            return False, None
        
        first_box = True

        for obj in self.objects:
            b, temp_box = obj.bounding_box(_time0, _time1)
            if not b:
                return False
            
            if first_box:
                output_box = temp_box
            else:
                output_box = surrounding_box(output_box, temp_box)

            first_box = False

        return True

