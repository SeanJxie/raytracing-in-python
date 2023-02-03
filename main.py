from vec import *
from camera import *

from scene_presets import *
from settings import *
from render import render_scene

if __name__ == "__main__":
    # World
    world = scattered_balls()

    # Image
    aspect_ratio = 3 / 2
    image_wt = 1000
    image_ht = int(image_wt / aspect_ratio)
    samples_per_pixel = 100
    max_depth = 10
    s = settings(image_wt, image_ht, samples_per_pixel, max_depth)

    # Camera
    lookfrom = vec3(6.0, 6.0, 6.0)
    lookat = vec3(0.0, 0.5, 0.0)
    vup = vec3(0, 1, 0)
    dist_to_focus = 10.0
    aperture = 0.1
    cam = camera(lookfrom, lookat, vup, 90, aspect_ratio, aperture, dist_to_focus)

    render_scene(world, cam, s)