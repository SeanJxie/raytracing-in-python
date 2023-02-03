import math
import random
import time
import datetime
from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
from PIL import Image

from vec import *
from ray import *
from hittablelist import *
from geometry import *
from camera import *
from colour import *
from material import *

from scene_presets import *
from settings import *

def ray_col(r: Ray, world: Hittable, depth: int) -> vec3:

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

    unit_dir = vec_unit(r.d)
    t = 0.5 * (unit_dir.y + 1.0)
    return vec_add(vec_smul(vec3(1.0, 1.0, 1.0), (1.0 - t)), vec_smul(vec3(0.5, 0.7, 1.0), t))

# Multiprocessing task
def render_scanline(scanline: list, world: HittableList, cam: Camera, samples: int, wt: int, ht: int, max_depth: int):
    j = scanline[0]
    rendered_scanline = []

    for i in scanline[1:]:
        # Sample and write 
        sampled_col_sum = vec3(0, 0, 0)
        for _ in range(samples):
            u = (i + random.random()) / (wt - 1)
            v = (j + random.random()) / (ht - 1)
            sampled_col_sum = vec_add(sampled_col_sum, ray_col(cam.get_ray(u, v), world, max_depth))

        rendered_scanline.append(compute_rgb_from_sample_sum(sampled_col_sum, samples))

    return rendered_scanline

def render_scene(world: HittableList, camera: Camera, settings: settings):
    samples = settings.samples
    wt = settings.wt
    ht = settings.ht
    max_depth = settings.max_depth

    coord_image = []
    for j in range(ht - 1, -1, -1):
        scanline = [j]
        for i in range(wt):
            scanline.append(i)
        coord_image.append(scanline)

    ntasks = len(coord_image)
    nprocs = cpu_count()
    image_data = []

    start = time.time()
    with Pool(nprocs) as p:
        # Makeshift "starmap" using imap and partial (so that progress can still be tracked and constant params are set)
        m = p.imap(partial(render_scanline, world=world, cam=camera, samples=samples, wt=wt, ht=ht, max_depth=max_depth), coord_image)
        for i, sl in enumerate(m, 1):
            print(f'Render progress: {i / ntasks:.2%}   ', end='\r')
            image_data.append(sl)
    dt = time.time() - start

    print(f"\nRender time ({nprocs} procs): {str(datetime.timedelta(seconds=dt))}")

    image = Image.fromarray(np.array(image_data, dtype=np.uint8))
    image.show()
    image.save(f'out.png')