import numpy as np

from vec import *

class ray:
    def __init__(self, origin: vec3, direction: vec3):
        self.orig = origin
        self.dir = direction

    def copy_assign(self, other: object) -> None:
        self.orig = other.orig
        self.dir = other.dir

    def origin(self) -> vec3:
        return self.orig

    def direction(self) -> vec3:
        return self.dir

    def at(self, t: float) -> vec3:
        return vec_add(self.orig, vec_smul(self.dir, t))

