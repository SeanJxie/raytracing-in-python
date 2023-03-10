import math
import random

class V3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, idx: int) -> float:
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y
        if idx == 2:
            return self.z
        raise IndexError

    def neg(self) -> object:
        return V3(-self.x, -self.y, -self.z)

    def len_sqr(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def len(self) -> float:
        return math.sqrt(self.len_sqr())

    def near_zero(self) -> bool:
        s = 1e-8
        return (math.fabs(self.x) < s) and (math.fabs(self.y) < s) and (math.fabs(self.z) < s)

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

def vec_add(u: V3, v: V3) -> V3:
    return V3(u.x + v.x, u.y + v.y, u.z + v.z)

def vec_sub(u: V3, v: V3) -> V3:
    return V3(u.x - v.x, u.y - v.y, u.z - v.z)

def vec_mul(u: V3, v: V3) -> V3:
    return V3(u.x * v.x, u.y * v.y, u.z * v.z)

def vec_smul(v: V3, t: float) -> V3:
    return V3(t * v.x, t * v.y, t * v.z)

def vec_sdiv(v: V3, t: float) -> V3:
    return vec_smul(v, 1 / t)

def vec_dot(u: V3, v: V3) -> float:
    return u.x * v.x + u.y * v.y + u.z * v.z

def vec_cross(u: V3, v: V3) -> V3:
    return V3(u.y * v.z - u.z * v.y,
                u.z * v.x - u.x * v.z,
                u.x * v.y - u.y * v.x)

def vec_unit(v: V3) -> V3:
    return vec_sdiv(v, v.len())

def vec_rand() -> V3:
    return V3(random.random(), random.random(), random.random())

def vec_rand_between(min: float, max: float) -> V3:
    return V3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))

def vec_rand_in_unit_sphere() -> V3:
    while 1:
        p = vec_rand_between(-1, 1)
        if p.len_sqr() >= 1:
            continue
        return p

def vec_rand_unit_in_unit_sphere() -> V3:
    return vec_unit(vec_rand_in_unit_sphere())

def vec_rand_in_unit_disk() -> V3:
    while 1:
        p = V3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        if p.len_sqr() >= 1:
            continue
        return p

def vec_reflect(v: V3, n: V3) -> V3:
    return vec_sub(v, vec_smul(n, 2 * vec_dot(v, n)))

def vec_refract(uv: V3, n: V3, etai_over_etat: float) -> V3:
    cos_theta = min(vec_dot(uv.neg(), n), 1.0)
    r_out_perp = vec_smul(vec_add(uv, vec_smul(n, cos_theta)), etai_over_etat)
    r_out_parallel = vec_smul(n, -math.sqrt(math.fabs(1.0 - r_out_perp.len_sqr())))

    return vec_add(r_out_perp, r_out_parallel)
