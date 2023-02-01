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

# Image
aspect_ratio = 16.0 / 9.0
image_wt = 400
image_ht = int(image_wt / aspect_ratio)
samples_per_pixel = 10
max_depth = 10

# World
world = hittable_list()

mat_ground = lambertian(vec3(0.8, 0.8, 0.8))
mat_center = lambertian(vec3(0.7, 0.3, 0.3))
mat_left   = metal(vec3(0.8, 0.8, 0.8), 0.3)
mat_right  = metal(vec3(0.8, 0.6, 0.2), 1.0)

world.add(sphere(vec3( 0.0, -100.5, -1.0), 100.0, mat_ground))
world.add(sphere(vec3( 0.0,    0.0, -1.0),   0.5, mat_center))
world.add(sphere(vec3(-1.0,    0.0, -1.0),   0.5, mat_left))
world.add(sphere(vec3( 1.0,    0.0, -1.0),   0.5, mat_right))

# Camera
cam = camera()

viewport_ht = 2.0
viewport_wt = aspect_ratio * viewport_ht
focal_length = 1.0

origin = vec3(0.0, 0.0, 0.0)
horizontal = vec3(viewport_wt, 0, 0)
vertical = vec3(0, viewport_ht, 0)

half_horizontal = vec_sdiv(horizontal, 2)
half_vertical = vec_sdiv(vertical, 2)
lower_left_corner = vec_sub(vec_sub(vec_sub(origin, half_horizontal), half_vertical), vec3(0, 0, focal_length))

image_data = np.zeros((image_ht, image_wt, 3), dtype=np.uint8)
print(f"Image dimensions: {image_wt}x{image_ht}")

start_time = time.time()
for j in range(image_ht - 1, -1, - 1):
    print(f'Scanlines remaining: {j}' + ' ' * len(str(image_ht)), end='\r')
    for i in range(image_wt):

        # Antialiasing!
        pixel_col = vec3(0, 0, 0)
        for s in range(samples_per_pixel):
            u = (i + random.random()) / (image_wt - 1)
            v = (j + random.random()) / (image_ht - 1)

            r = cam.get_ray(u, v)
            pixel_col = vec_add(pixel_col, ray_col(r, world, max_depth))

        # image_ht - j - 1 for upside-down flip
        write_col(image_data, i, image_ht - j - 1, pixel_col, samples_per_pixel)

dt = time.time() - start_time
print('\nDone.')
print(f'Render time: {str(datetime.timedelta(seconds=dt))}')

image = Image.fromarray(image_data)
image.show()
image.save('out.png')
