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
from sphere import *
from camera import *
from colour import *
from material import *

from scene_presets import *
from settings import *

def ray_col(r: Ray, bg_col: V3, world: Hittable, depth: int) -> V3:

    # If we've exceeded the ray bounce limit, no more light is gathered.
    if depth <= 0:
        return V3(0, 0, 0)

    # 0.001 gets rid of shadow acne
    has_hit, rec = world.hit(r, 0.001, math.inf)

    if not has_hit:
        return bg_col
    
    emitted = rec.material.emitted(rec.u, rec.v, rec.p)

    has_scatter, attenuation, scattered = rec.material.scatter(r, rec)
    if not has_scatter:
        return emitted
    
    return vec_add(emitted, vec_mul(attenuation, ray_col(scattered, bg_col, world, depth - 1)))


# Multiprocessing task
def render_scanline(scanline: list, world: HittableList, cam: Camera, bg_col: V3, samples: int, wt: int, ht: int, max_depth: int):
    j = scanline[0]
    rendered_scanline = []

    for i in scanline[1:]:
        # Sample and write 
        sampled_col_sum = V3(0, 0, 0)
        for _ in range(samples):
            u = (i + random.random()) / (wt - 1)
            v = (j + random.random()) / (ht - 1)
            sampled_col_sum = vec_add(sampled_col_sum, ray_col(cam.get_ray(u, v), bg_col, world, max_depth))

        rendered_scanline.append(compute_rgb_from_sample_sum(sampled_col_sum, samples))

    return rendered_scanline

def render_scene(world: HittableList, camera: Camera, settings: Settings):
    samples = settings.samples
    wt = settings.wt
    ht = settings.ht
    bg_col = settings.bg_col
    max_depth = settings.max_depth

    print("Setting up...")
    coord_image = []
    for j in range(ht - 1, -1, -1):
        scanline = [j]
        for i in range(wt):
            scanline.append(i)
        coord_image.append(scanline)

    ntasks = len(coord_image)
    nprocs = cpu_count()
    image_data = []
    print("Done.")

    print("\nRendering...")
    print(f'Render progress: 0.00%', end='\r')
    start = time.time()
    with Pool(nprocs) as p:
        # Makeshift "starmap" using imap and partial (so that progress can still be tracked and constant params are set)
        m = p.imap(partial(render_scanline, world=world, cam=camera, bg_col=bg_col, samples=samples, wt=wt, ht=ht, max_depth=max_depth), coord_image)
        for i, sl in enumerate(m, 1):
            print(f'Render progress: {i / ntasks:.2%}   ', end='\r')
            image_data.append(sl)
    dt = time.time() - start

    print("\nDone.")
    print(f"Render time ({nprocs} procs): {str(datetime.timedelta(seconds=dt))}")

    print("\nSaving image...")
    image = Image.fromarray(np.array(image_data, dtype=np.uint8))
    image.save(f'out.png')
    print("Done.")
    image.show()