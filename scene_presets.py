import random

from hittable_list import *
from material import *
from vec import *
from geometry import *

random.seed(1234)

def scattered_balls() -> hittable_list:

    world = hittable_list()

    ground_material = lambertian(vec3(0.5, 0.5, 0.5))
    world.add(sphere(vec3(0, -1000, 0), 1000, ground_material))

    # Bunch of small spheres
    for a in range(-11, 12):
        for b in range(-11, 12):
            choose_mat = random.random()
            center = vec3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if vec_sub(center, vec3(4, 0.2, 0)).len() > 0.9:
                
                if choose_mat < 0.8:
                    albedo = vec_mul(vec3.rand(), vec3.rand())
                    sphere_material = lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_material))

                elif choose_mat < 0.95:
                    albedo = vec3.rand_between(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_material))

                else:
                    sphere_material = dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_material))

    # Three big spheres
    material1 = dielectric(1.5)
    world.add(sphere(vec3(0, 1, 0), 1.0, material1))

    material2 = lambertian(vec3(0.4, 0.2, 0.1))
    world.add(sphere(vec3(-4, 1, 0), 1.0, material2))

    material3 = metal(vec3(0.7, 0.6, 0.5), 0.0)
    world.add(sphere(vec3(4, 1, 0), 1.0, material3))
    
    return world

def tri() -> hittable_list:
    world = hittable_list()

    ground_material = lambertian(vec3(0.5, 0.5, 0.5))
    world.add(sphere(vec3(0, -1000, 0), 1000, ground_material))

    material1 = metal(vec3(0.7, 0.6, 0.5), 0.0)
    world.add(triangle(vec3(0, 1, 0), vec3(1, 1, 0), vec3(0, 1, 2), material1))

    return world
