from hittable import *

class hittable_list(hittable):
    def __init__(self) -> None:
        self.objects = []

    def clear(self) -> None:
        self.objects.clear()

    def add(self, obj: hittable) -> None:
        self.objects.append(obj)

    def hit(self, r: ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max

        for obj in self.objects:
            if obj.hit(r, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t

                # Set rec to temp rec
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.t = temp_rec.t
                rec.front_face = temp_rec.front_face
                rec.material = temp_rec.material

        return hit_anything
