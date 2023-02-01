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

class dielectric(material):
    def __init__(self, index_of_refraction: float) -> None:
        self.ir = index_of_refraction

    def scatter(self, r_in: ray, rec: hit_record, attenuation: vec3, scattered: ray) -> bool:
        attenuation.copy_assign(vec3(1.0, 1.0, 1.0))
        
        if rec.front_face:
            refraction_ratio = 1.0 / self.ir
        else:
            refraction_ratio = self.ir

        unit_dir = vec_unit(r_in.direction())
        cos_theta = min(vec_dot(unit_dir.neg(), rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0

        if cannot_refract or (self._reflectance(cos_theta, refraction_ratio) > random.random()):
            direction = reflect(unit_dir, rec.normal)
        else:
            direction = refract(unit_dir, rec.normal, refraction_ratio)

        scattered.copy_assign(ray(rec.p, direction))

        return True

    @staticmethod
    def _reflectance(cosine: float, ref_idx: float) -> float:
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0

        return r0 + (1 - r0) * pow((1 - cosine), 5)