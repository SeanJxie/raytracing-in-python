from vec import *

class Ray:
    def __init__(self, o: V3, d: V3, time: float):
        self.o = o
        self.d = d
        self.time = time

    def at(self, t: float) -> V3:
        return vec_add(self.o, vec_smul(self.d, t))
