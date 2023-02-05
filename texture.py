from PIL import Image

from vec import *
from perlin import *
from util import *

# Template
class Texture:
    def value(self, u: float, v: float, p: V3) -> V3:
        pass

class SolidColourTex(Texture):
    def __init__(self, c: V3) -> None:
        self.colour_value = c

    def value(self, u: float, v: float, p: V3) -> V3:
        return self.colour_value
    
class CheckeredTex(Texture):
    def __init__(self, _even: Texture, _odd: Texture) -> None:
        self.even = _even
        self.odd = _odd

    def value(self, u: float, v: float, p: V3) -> V3:
        sines = math.sin(10 * p.x) * math.sin(10 * p.y) * math.sin(10 * p.z)
        if sines < 0:
            return self.odd.value(u, v, p)
        return self.even.value(u, v, p)
    
class NoiseTex(Texture):
    def __init__(self, scale: float) -> None:
        self.scale = scale
        self.noise = Perlin()

    def value(self, u: float, v: float, p: V3) -> V3:
        return vec_smul(V3(1, 1, 1), 0.5 * (1 + math.sin(self.scale * p.z + 10 * self.noise.turbulance(p))))
    
class ImageTex(Texture):
    def __init__(self, filename: str) -> None:        
        self._image = Image.open(filename).convert("RGB")
        self._width = self._image.width
        self._height = self._image.height

    def __del__(self) -> None:
        self._image.close()

    def value(self, u: float, v: float, p: V3) -> V3:
        if self._image == None:
            # Bright red for debug
            return V3(1, 0, 0)
        
        u = clamp(u, 0.0, 1.0)
        v = 1.0 - clamp(v, 0.0, 1.0)

        i = int(u * self._width)
        j = int(v * self._height)

        if i >= self._width:
            i = self._width - 1
        
        if j >= self._height:
            j = self._height - 1

        pixel = self._image.getpixel((i, j))
        
        col_scale = 1 / 255
        return V3(pixel[0] * col_scale, pixel[1] * col_scale, pixel[2] * col_scale)