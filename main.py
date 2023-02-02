import math
import random
import time
import datetime

import numpy as np
from PIL import Image

from vec import *
from ray import *
from hittable_list import *
from sphere import *
from camera import *
from colour import *
from material import *

from scene_presets import random_scene

# Image
aspect_ratio = 3 / 2
image_wt = 1000
image_ht = int(image_wt / aspect_ratio)
samples_per_pixel = 1
max_depth = 10

# World
world = random_scene()

# Camera
lookfrom = vec3(13, 2, 3)
lookat = vec3(0, 0, 0)
vup = vec3(0, 1, 0)
dist_to_focus = 10.0
aperture = 0.1

cam = camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)


def ray_col(r: ray, world: hittable, depth: int) -> vec3:
    rec = hit_record()

    # If we've exceeded the ray bounce limit, no more light is gathered.
    if depth <= 0:
        return vec3(0, 0, 0)

    # 0.001 gets rid of shadow acne
    if world.hit(r, 0.001, math.inf, rec):
        scattered = ray(None, None)
        attenuation = vec3(None, None, None)

        if rec.material.scatter(r, rec, attenuation, scattered):
            return vec_mul(attenuation, ray_col(scattered, world, depth - 1))

    unit_dir = vec_unit(r.direction())
    t = 0.5 * (unit_dir.y() + 1.0)
    return vec_add(vec_smul(vec3(1.0, 1.0, 1.0), (1.0 - t)), vec_smul(vec3(0.5, 0.7, 1.0), t))


def main():
    # Set up a live window to watch the render
    import pygame as pg
    import sys

    surface = pg.display.set_mode((image_wt, image_ht))
    pg.display.set_caption("Live Render")

    print(f"Image dimensions: {image_wt}x{image_ht}")

    image_data = np.zeros((image_ht, image_wt, 3), dtype=np.uint8)

    start_time = time.time()

    for j in range(image_ht - 1, -1, -1):
        print(f'Scanlines remaining: {j}' + '   ', end='\r')
        for i in range(image_wt):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.quit()
                    sys.exit()
            
            # Antialias
            pixel_col = vec3(0, 0, 0)
            for _ in range(samples_per_pixel):
                u = (i + random.random()) / (image_wt - 1)
                v = (j + random.random()) / (image_ht - 1)

                r = cam.get_ray(u, v)
                pixel_col = vec_add(pixel_col, ray_col(r, world, max_depth))
            
            write_col_to_pygame_surface(surface, i, image_ht - j - 1, pixel_col, samples_per_pixel)

            pg.display.update()

    dt = time.time() - start_time

    print('\nDone.')
    print(f'Render time: {str(datetime.timedelta(seconds=dt))}')

    image = Image.fromarray(image_data)
    image.show()
    image.save(f'out.png')

    
if __name__ == '__main__':
    main()

   