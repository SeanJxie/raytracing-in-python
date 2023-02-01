import math
import random

class vec3:
    def __init__(self, e0: float, e1: float, e2: float) -> None:
        self.e0 = e0
        self.e1 = e1
        self.e2 = e2
        self.e = [e0, e1, e2]

    def copy_assign(self, other: object) -> None:
        self.e0 = other.e0
        self.e1 = other.e1
        self.e2 = other.e2
        self.e = other.e

    def as_list(self) -> list:
        return self.e

    def x(self) -> float:
        return self.e[0]

    def y(self) -> float:
        return self.e[1]

    def z(self) -> float:
        return self.e[2]

    def neg(self) -> object:
        return vec3(-self.e0, -self.e1, -self.e2)

    def at(self, i) -> float:
        return self.e[i]

    def __add__(self, v) -> object:
        self.e[0] += v.e[0]
        self.e[1] += v.e[1]
        self.e[2] += v.e[2]

        return self

    def __mul__(self, v) -> object:
        self.e[0] *= v.e[0]
        self.e[1] *= v.e[1]
        self.e[2] *= v.e[2]

        return self

    def __div__(self, t: float) -> object:
        self = self * (1 / t)
        return self

    def len_sqr(self) -> float:
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

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
        print(f"({self.e[0]}, {self.e[1]}, {self.e[2]})")


def vec_add(u: vec3, v: vec3) -> vec3:
    return vec3(u.e[0] + v.e[0], u.e[1] + v.e[1], u.e[2] + v.e[2])

def vec_sub(u: vec3, v: vec3) -> vec3:
    return vec3(u.e[0] - v.e[0], u.e[1] - v.e[1], u.e[2] - v.e[2])

def vec_mul(u: vec3, v: vec3) -> vec3:
    return vec3(u.e[0] * v.e[0], u.e[1] * v.e[1], u.e[2] * v.e[2])

def vec_smul(v: vec3, t: float) -> vec3:
    return vec3(t * v.e[0], t * v.e[1], t * v.e[2])

def vec_sdiv(v: vec3, t: float) -> vec3:
    return vec_smul(v, 1 / t)

def vec_dot(u: vec3, v: vec3) -> float:
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]

def vec_cross(u: vec3, v: vec3) -> vec3:
    return vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
                u.e[2] * v.e[0] - u.e[0] * v.e[2],
                u.e[0] * v.e[1] - u.e[1] * v.e[0])

def vec_unit(v: vec3) -> vec3:
    return vec_sdiv(v, v.len())

def random_in_unit_sphere() -> vec3:
    while (1):
        p = vec3.rand_between(-1, 1)
        if p.len_sqr() >= 1:
            continue
        return p

def random_unit_in_unit_sphere() -> vec3:
    return vec_unit(random_in_unit_sphere())

def reflect(v: vec3, n: vec3) -> vec3:
    return vec_sub(v, vec_smul(n, 2 * vec_dot(v, n)))