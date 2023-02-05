import math

from vec import *
from util import *

def compute_rgb_from_sample_sum(col: V3, samples_per_pixel: int) -> list:
    r = col.x
    g = col.y
    b = col.z

    scale = 1.0 / samples_per_pixel
    r = math.sqrt(scale * r)
    g = math.sqrt(scale * g)
    b = math.sqrt(scale * b)

    return [
        int(256 * clamp(r, 0.0, 0.999)), 
        int(256 * clamp(g, 0.0, 0.999)), 
        int(256 * clamp(b, 0.0, 0.999))
    ]
