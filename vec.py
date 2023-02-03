import math
import random

class vec3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def neg(self) -> object:
        return vec3(-self.x, -self.y, -self.z)

    def len_sqr(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def len(self) -> float:
        return math.sqrt(self.len_sqr())

    def near_zero(self) -> bool:
        s = 1e-8
        return (math.fabs(self.x) < s) and (math.fabs(self.y) < s) and (math.fabs(self.z) < s)

    def __str__(self) -> None:
        print(f"({self.x}, {self.y}, {self.z})")

def vec_add(u: vec3, v: vec3) -> vec3:
    return vec3(u.x + v.x, u.y + v.y, u.z + v.z)

def vec_sub(u: vec3, v: vec3) -> vec3:
    return vec3(u.x - v.x, u.y - v.y, u.z - v.z)

def vec_mul(u: vec3, v: vec3) -> vec3:
    return vec3(u.x * v.x, u.y * v.y, u.z * v.z)

def vec_smul(v: vec3, t: float) -> vec3:
    return vec3(t * v.x, t * v.y, t * v.z)

def vec_sdiv(v: vec3, t: float) -> vec3:
    return vec_smul(v, 1 / t)

def vec_dot(u: vec3, v: vec3) -> float:
    return u.x * v.x + u.y * v.y + u.z * v.z

def vec_cross(u: vec3, v: vec3) -> vec3:
    return vec3(u.y * v.z - u.z * v.y,
                u.z * v.x - u.x * v.z,
                u.x * v.y - u.y * v.x)

def vec_unit(v: vec3) -> vec3:
    return vec_sdiv(v, v.len())

def vec_rand() -> vec3:
    return vec3(random.random(), random.random(), random.random())

def vec_rand_between(min: float, max: float) -> vec3:
    return vec3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))

def vec_rand_in_unit_sphere() -> vec3:
    while 1:
        p = vec_rand_between(-1, 1)
        if p.len_sqr() >= 1:
            continue
        return p

def vec_rand_unit_in_unit_sphere() -> vec3:
    return vec_unit(vec_rand_in_unit_sphere())

def vec_rand_in_unit_disk() -> vec3:
    while 1:
        p = vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        if p.len_sqr() >= 1:
            continue
        return p

def vec_reflect(v: vec3, n: vec3) -> vec3:
    return vec_sub(v, vec_smul(n, 2 * vec_dot(v, n)))

def vec_refract(uv: vec3, n: vec3, etai_over_etat: float) -> vec3:
    cos_theta = min(vec_dot(uv.neg(), n), 1.0)
    r_out_perp = vec_smul(vec_add(uv, vec_smul(n, cos_theta)), etai_over_etat)
    r_out_parallel = vec_smul(n, -math.sqrt(math.fabs(1.0 - r_out_perp.len_sqr())))

    return vec_add(r_out_perp, r_out_parallel)

