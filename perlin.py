import random

from vec import *

class Perlin:
    def __init__(self) -> None:
        self._point_count = 256
        self._ranvec = [vec_unit(vec_rand_between(-1, 1)) for _ in range(self._point_count)]

        self.perm_x = self._perlin_generate_perm()
        self.perm_y = self._perlin_generate_perm()
        self.perm_z = self._perlin_generate_perm()

    def noise(self, p: V3) -> float:
        u = p.x - math.floor(p.x)
        v = p.y - math.floor(p.y)
        w = p.z - math.floor(p.z)
        i = math.floor(p.x)
        j = math.floor(p.y)
        k = math.floor(p.z)

        c = [[[self._ranvec[self.perm_x[(i + di) & 255] ^ self.perm_y[(j + dj) & 255] ^ self.perm_z[(k + dk) & 255]] 
                for dk in range(2)] 
                for dj in range(2)] 
                for di in range(2)]

        return self._perlin_interp(c, u, v, w)
    
    def turbulance(self, p: V3, depth: int=7) -> float:
        accum = 0.0
        temp_p = p
        weight = 1.0

        for _ in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p = vec_smul(temp_p, 2)

        return math.fabs(accum)

    def _perlin_generate_perm(self) -> list[int]:
        p = []
        for i in range(self._point_count):
            p.append(i)
        return self._permute(p, self._point_count)

    @staticmethod
    def _perlin_interp(c: list[list[list[float]]], u: float, v: float, w: float) -> float:
        uu = u * u * (3 - 2 * u)
        vv = v * v * (3 - 2 * v)
        ww = w * w * (3 - 2 * w)
        accum = 0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = V3(u - i, v - j, w - k)
                    accum += (i * uu + (1 - i) * (1 - uu)) * (j * vv + (1 - j) * (1 - vv)) * (k * ww + (1 - k) * (1 - ww)) * vec_dot(c[i][j][k], weight_v)
        return accum 

    @staticmethod
    def _trilinear_interp(c: list[list[list[float]]], u: float, v: float, w: float) -> float:
        accum = 0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    accum += (i * u + (1 - i) * (1 - u)) * (j * v + (1 - j) * (1 - v)) * (k * w + (1 - k) * (1 - w)) * c[i][j][k]
        return accum     
                
    @staticmethod
    def _permute(p: list[int], n: int) -> list[int]:
        for i in range(n - 1, 0, -1):
            target = random.randint(0, i)
            p[i], p[target] = p[target], p[i]

        return p
