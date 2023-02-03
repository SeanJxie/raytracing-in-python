import math
import random

class vec3:
    def __init__(self, e0: float, e1: float, e2: float) -> None:
        self.e0 = e0
        self.e1 = e1
        self.e2 = e2

    def copy_assign(self, other: object) -> None:
        self.e0 = other.e0
        self.e1 = other.e1
        self.e2 = other.e2

    def as_list(self) -> list:
        return [self.e0, self.e1, self.e2]

    def x(self) -> float:
        return self.e0

    def y(self) -> float:
        return self.e1

    def z(self) -> float:
        return self.e2

    def neg(self) -> object:
        return vec3(-self.e0, -self.e1, -self.e2)

    def len_sqr(self) -> float:
        return self.e0 * self.e0 + self.e1 * self.e1 + self.e2 * self.e2

    def len(self) -> float:
        return math.sqrt(self.len_sqr())

    def near_zero(self) -> bool:
        s = 1e-8
        return (math.fabs(self.e0) < s) and (math.fabs(self.e1) < s) and (math.fabs(self.e2) < s)

    @staticmethod
    def rand() -> object:
        return vec3(random.random(), random.random(), random.random())

    @staticmethod
    def rand_between(min: float, max: float) -> object:
        return vec3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))

    def __str__(self) -> None:
        print(f"({self.e0}, {self.e1}, {self.e2})")


def vec_add(u: vec3, v: vec3) -> vec3:
    return vec3(u.e0 + v.e0, u.e1 + v.e1, u.e2 + v.e2)

def vec_sub(u: vec3, v: vec3) -> vec3:
    return vec3(u.e0 - v.e0, u.e1 - v.e1, u.e2 - v.e2)

def vec_mul(u: vec3, v: vec3) -> vec3:
    return vec3(u.e0 * v.e0, u.e1 * v.e1, u.e2 * v.e2)

def vec_smul(v: vec3, t: float) -> vec3:
    return vec3(t * v.e0, t * v.e1, t * v.e2)

def vec_sdiv(v: vec3, t: float) -> vec3:
    return vec_smul(v, 1 / t)

def vec_dot(u: vec3, v: vec3) -> float:
    return u.e0 * v.e0 + u.e1 * v.e1 + u.e2 * v.e2

def vec_cross(u: vec3, v: vec3) -> vec3:
    return vec3(u.e1 * v.e2 - u.e2 * v.e1,
                u.e2 * v.e0 - u.e0 * v.e2,
                u.e0 * v.e1 - u.e1 * v.e0)

def vec_unit(v: vec3) -> vec3:
    return vec_sdiv(v, v.len())

def random_in_unit_sphere() -> vec3:
    while 1:
        p = vec3.rand_between(-1, 1)
        if p.len_sqr() >= 1:
            continue
        return p

def random_unit_in_unit_sphere() -> vec3:
    return vec_unit(random_in_unit_sphere())

def random_in_unit_disk() -> vec3:
    while 1:
        p = vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        if p.len_sqr() >= 1:
            continue
        return p

def reflect(v: vec3, n: vec3) -> vec3:
    return vec_sub(v, vec_smul(n, 2 * vec_dot(v, n)))

def refract(uv: vec3, n: vec3, etai_over_etat: float) -> vec3:
    cos_theta = min(vec_dot(uv.neg(), n), 1.0)
    r_out_perp = vec_smul(vec_add(uv, vec_smul(n, cos_theta)), etai_over_etat)
    r_out_parallel = vec_smul(n, -math.sqrt(math.fabs(1.0 - r_out_perp.len_sqr())))

    return vec_add(r_out_perp, r_out_parallel)

