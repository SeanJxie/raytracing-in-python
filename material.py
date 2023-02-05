from vec import *
from ray import *

from hittable import HitRecord
from texture import *

class Material:
    def scatter(self, r_in: Ray, rec: HitRecord) -> tuple[bool, V3, Ray]:
        pass

    def emitted(self, u: float, v: float, p: V3) -> V3:
        pass

class Lambertian(Material):
    def __init__(self, albedo: Texture) -> None:
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> tuple[bool, V3, Ray]:
        scatter_dir = vec_add(rec.normal, vec_rand_unit_in_unit_sphere())

        if scatter_dir.near_zero():
            scatter_dir = rec.normal

        scattered = Ray(rec.p, scatter_dir, r_in.time)
        attenuation = self.albedo.value(rec.u, rec.v, rec.p)

        return True, attenuation, scattered

    def emitted(self, u: float, v: float, p: V3) -> V3:
        return V3(0, 0, 0)

class Metal(Material):
    def __init__(self, albedo: Texture, fuzz: float) -> None:
        self.albedo = albedo
        
        if fuzz < 1:
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, r_in: Ray, rec: HitRecord) -> tuple[bool, V3, Ray]:
        reflected = vec_reflect(vec_unit(r_in.d), rec.normal)
        attenuation = self.albedo.value(rec.u, rec.v, rec.p)
        scattered = Ray(rec.p, vec_add(reflected, vec_smul(vec_rand_in_unit_sphere(), self.fuzz)), r_in.time)
        
        return vec_dot(scattered.d, rec.normal) > 0, attenuation, scattered
    
    def emitted(self, u: float, v: float, p: V3) -> V3:
        return V3(0, 0, 0)

class Dielectric(Material):
    def __init__(self, index_of_refraction: float) -> None:
        self.ir = index_of_refraction

    def scatter(self, r_in: Ray, rec: HitRecord) -> tuple[bool, V3, Ray]:
        
        if rec.front_face:
            refraction_ratio = 1.0 / self.ir
        else:
            refraction_ratio = self.ir

        unit_dir = vec_unit(r_in.d)
        cos_theta = min(vec_dot(unit_dir.neg(), rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0

        if cannot_refract or (self._reflectance(cos_theta, refraction_ratio) > random.random()):
            direction = vec_reflect(unit_dir, rec.normal)
        else:
            direction = vec_refract(unit_dir, rec.normal, refraction_ratio)

        attenuation = V3(1.0, 1.0, 1.0)
        scattered = Ray(rec.p, direction, r_in.time)

        return True, attenuation, scattered

    def emitted(self, u: float, v: float, p: V3) -> V3:
        return V3(0, 0, 0)

    @staticmethod
    def _reflectance(cosine: float, ref_idx: float) -> float:
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0

        return r0 + (1 - r0) * pow((1 - cosine), 5)
    
class DiffuseLight(Material):
    def __init__(self, emit: Texture) -> None:
        self.emit = emit

    def scatter(self, r_in: Ray, rec: HitRecord) -> tuple[bool, V3, Ray]:
        return False, None, None
    
    def emitted(self, u: float, v: float, p: V3) -> V3:
        return self.emit.value(u, v, p)
    
class Isotropic(Material):
    def __init__(self, albedo: Texture) -> None:
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> tuple[bool, V3, Ray]:
        attenuation = self.albedo.value(rec.u, rec.v, rec.p)
        scattered = Ray(rec.p, vec_rand_in_unit_sphere(), r_in.time)

        return True, attenuation, scattered
    
    def emitted(self, u: float, v: float, p: V3) -> V3:
        return self.emit.value(u, v, p)
    