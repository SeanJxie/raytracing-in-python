from vec import *
from camera import *

from scene_presets import *
from settings import *
from render import render_scene

def main():
    # Image
    aspect_ratio = 1.0
    image_wt = 800
    image_ht = int(image_wt / aspect_ratio)
    samples_per_pixel = 500
    max_depth = 1000
    bg_col = V3(0, 0, 0)
    s = Settings(image_wt, image_ht, bg_col, samples_per_pixel, max_depth)

    # World
    world, cam = artwork()

    render_scene(world, cam, s)

if __name__ == '__main__':
    main()