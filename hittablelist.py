from hittable import *

class HittableList(Hittable):
    def __init__(self) -> None:
        self.objects = []

    def clear(self) -> None:
        self.objects.clear()

    def add(self, obj: Hittable) -> None:
        self.objects.append(obj)

    def hit(self, r: Ray, t_min: float, t_max: float) -> bool:
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
                rec.front_face = temp_rec.front_face
                rec.material = temp_rec.material

        return hit_anything, rec
