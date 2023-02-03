from vec import *

class Ray:
    def __init__(self, o: vec3, d: vec3):
        self.o = o
        self.d = d

    def at(self, t: float) -> vec3:
        return vec_add(self.o, vec_smul(self.d, t))
