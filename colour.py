import math

import numpy as np

from vec import *
from util import *

def write_col(image_data: np.ndarray, i: int, j: int, col: vec3, samples_per_pixel: int) -> None:
    r = col.x()
    g = col.y()
    b = col.z()

    scale = 1.0 / samples_per_pixel
    r = math.sqrt(scale * r)
    g = math.sqrt(scale * g)
    b = math.sqrt(scale * b)

    image_data[j, i] = [
        int(256 * clamp(r, 0.0, 0.999)), 
        int(256 * clamp(g, 0.0, 0.999)), 
        int(256 * clamp(b, 0.0, 0.999))
    ]
