import math
import random
import time
import datetime

import numpy as np
from PIL import Image

from vec import *
from ray import *
from hittable_list import *
from geometry import *
from camera import *
from colour import *
from material import *

from scene_presets import *
from model_loader import *

# Image
aspect_ratio = 3 / 2
image_wt = 500
image_ht = int(image_wt / aspect_ratio)
samples_per_pixel = 100
max_depth = 10

# World
world = scattered_balls()

# Camera
lookfrom = vec3(13.0, 2.0, 3.0)
lookat = vec3(0.0, 0.0, 0.0)
vup = vec3(0, 1, 0)
dist_to_focus = 10.0
aperture = 0.1

cam = camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

def ray_col(r: ray, world: hittable, depth: int) -> vec3:

    # If we've exceeded the ray bounce limit, no more light is gathered.
    if depth <= 0:
        return vec3(0, 0, 0)

    # 0.001 gets rid of shadow acne
    has_hit, rec = world.hit(r, 0.001, math.inf)
    if has_hit:
        has_scattered, attenuation, scattered = rec.material.scatter(r, rec)

        if has_scattered:
            return vec_mul(attenuation, ray_col(scattered, world, depth - 1))

        return vec3(0, 0, 0)

    unit_dir = vec_unit(r.direction())
    t = 0.5 * (unit_dir.y() + 1.0)
    return vec_add(vec_smul(vec3(1.0, 1.0, 1.0), (1.0 - t)), vec_smul(vec3(0.5, 0.7, 1.0), t))


# RENDER CODE
def render_scanline(scanline: list):
    rendered_scanline = []
    j = scanline[0]

    for i in scanline[1:]:
        # Sample and write 
        pixel_col = vec3(0, 0, 0)
        for _ in range(samples_per_pixel):
            u = (i + random.random()) / (image_wt - 1)
            v = (j + random.random()) / (image_ht - 1)

            r = cam.get_ray(u, v)
            pixel_col = vec_add(pixel_col, ray_col(r, world, max_depth))
        
        r = pixel_col.x()
        g = pixel_col.y()
        b = pixel_col.z()

        scale = 1.0 / samples_per_pixel
        r = math.sqrt(scale * r)
        g = math.sqrt(scale * g)
        b = math.sqrt(scale * b)

        rendered_scanline.append([
            int(256 * clamp(r, 0.0, 0.999)), 
            int(256 * clamp(g, 0.0, 0.999)), 
            int(256 * clamp(b, 0.0, 0.999))
        ])

    return rendered_scanline


if __name__ == '__main__':
    from multiprocessing import Pool

    coord_image = []
    for j in range(image_ht - 1, -1, -1):
        scanline = [j]
        for i in range(image_wt):
            scanline.append(i)
        coord_image.append(scanline)

    ntasks = len(coord_image)
    nprocs = 7
    image_data = []

    start = time.time()
    with Pool(nprocs) as p:
        for i, sl in enumerate(p.imap(render_scanline, coord_image), 1):
            print(f'Render progress: {i / ntasks:.2%}  ', end='\r')
            image_data.append(sl)

    dt = time.time() - start
    print(f"\nRender time ({nprocs} procs): {str(datetime.timedelta(seconds=dt))}")

    image = Image.fromarray(np.array(image_data, dtype=np.uint8))
    image.show()
    image.save(f'out.png')
