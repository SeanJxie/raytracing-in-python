from vec import *
from ray import *

from hittable import *

class material:
    def scatter(self, r_in: ray, rec: hit_record, attenuation: vec3, scattered: ray) -> bool:
        pass

class lambertian(material):
    def __init__(self, albedo: vec3) -> None:
        self.albedo = albedo

    def scatter(self, r_in: ray, rec: hit_record, attenuation: vec3, scattered: ray) -> bool:
        scatter_dir = vec_add(rec.normal, random_unit_in_unit_sphere())

        if scatter_dir.near_zero():
            scatter_dir = rec.normal

        scattered.copy_assign(ray(rec.p, scatter_dir))
        attenuation.copy_assign(self.albedo)

        return True

class metal(material):
    def __init__(self, albedo: vec3, fuzz: float) -> None:
        self.albedo = albedo
        
        if fuzz < 1:
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, r_in: ray, rec: hit_record, attenuation: vec3, scattered: ray) -> bool:
        reflected = reflect(vec_unit(r_in.direction()), rec.normal)
        scattered.copy_assign(ray(rec.p, vec_add(reflected, vec_smul(random_in_unit_sphere(), self.fuzz))))
        attenuation.copy_assign(self.albedo)
        
        return vec_dot(scattered.direction(), rec.normal) > 0