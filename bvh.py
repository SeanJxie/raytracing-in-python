from random import randint

from hittable import *
from hittablelist import *

from functools import cmp_to_key

class BVHnode(Hittable):
    def __init__(self, lst: HittableList, start: int, end: int, time0: float, time1: float) -> None:
        axis = randint(0, 2)

        if axis == 0:
            compatator = box_x_compare
        elif axis == 1:
            compatator = box_y_compare
        else:
            compatator = box_z_compare

        object_span = end - start
        if object_span == 1:
            self.left = lst.objects[start]
            self.right = lst.objects[start]
        elif object_span == 2:
            if compatator(lst.objects[start], lst.objects[start + 1]):
                self.left = lst.objects[start]
                self.right = lst.objects[start + 1]
            else:
                self.left = lst.objects[start + 1]
                self.right = lst.objects[start]
        else:
            lst.objects.sort(key=cmp_to_key(compatator))
            
            mid = start + object_span // 2
            self.left = BVHnode(lst, start, mid, time0, time1)
            self.right = BVHnode(lst, mid, end, time0, time1)

        b1, box_left = self.left.bounding_box(time0, time1)
        b2, box_right = self.right.bounding_box(time0, time1)

        if not (b1 and b2):
            print("ERROR: No bounding box in BVHNode __init__.")

        self.box = surrounding_box(box_left, box_right)
    
    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord]:
        if not self.box.hit(r, t_min, t_max):
            return False, None

        hit_left, rec_left = self.left.hit(r, t_min, t_max)
        if hit_left:
            hit_right, rec_right = self.right.hit(r, t_min, rec_left.t)
        else:
            hit_right, rec_right = self.right.hit(r, t_min, t_max)

        if hit_left:
            return True, rec_left
        if hit_right:
            return True, rec_right
        return False, None

    def bounding_box(self, _time0: float, _time1: float) -> tuple[bool, AABB]:
        return True, self.box
    
def box_compare(a: Hittable, b: Hittable, axis: int) -> bool:
    b1, box_a = a.bounding_box(0, 0)
    b2, box_b = b.bounding_box(0, 0)

    if not b1 or not b2:
        print("ERROR: No bounding box in BVHNode __init__.")

    if axis == 0:
        return box_a.mini.x < box_b.mini.x

    if axis == 1:
        return box_a.mini.y < box_b.mini.y
    
    return box_a.mini.z < box_b.mini.z

def box_x_compare(a: Hittable, b: Hittable) -> bool:
    return box_compare(a, b, 0)

def box_y_compare(a: Hittable, b: Hittable) -> bool:
    return box_compare(a, b, 1)

def box_z_compare(a: Hittable, b: Hittable) -> bool:
    return box_compare(a, b, 2)