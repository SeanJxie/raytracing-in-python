from vec import *
from camera import *

from scene_presets import *
from settings import *
from render import render_scene

def main():
    # World
    world = scattered_spheres()

    # Image
    aspect_ratio = 1.0
    image_wt = 500
    image_ht = int(image_wt / aspect_ratio)
    samples_per_pixel = 50
    max_depth = 10
    bg_col = V3(1, 1, 1)
    s = Settings(image_wt, image_ht, bg_col, samples_per_pixel, max_depth)

    # Camera
    lookfrom = V3(13, 2, 3)
    lookat = V3(0, 0, 0)
    vup = V3(0, 1, 0)
    dist_to_focus = 10
    aperture = 0.1
    fov = 20
    cam = Camera(lookfrom, lookat, vup, fov, aspect_ratio, aperture, dist_to_focus, 0.0, 1.0)

    render_scene(world, cam, s)

if __name__ == '__main__':
    main()