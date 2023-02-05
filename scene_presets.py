import random

from hittablelist import *
from material import *
from vec import *

from sphere import *
from aarect import *
from box import *

random.seed(1234)

def scattered_spheres() -> HittableList:
    world = HittableList()

    checkered = CheckeredTex(SolidColourTex(V3(0.2, 0.3, 0.1)), SolidColourTex(V3(0.9, 0.9, 0.9)))
    ground_material = Lambertian(checkered)
    world.add(Sphere(V3(0, -1000, 0), 1000, ground_material))

    # Bunch of small spheres
    for a in range(-11, 12):
        for b in range(-11, 12):
            choose_mat = random.random()
            center = V3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if vec_sub(center, V3(4, 0.2, 0)).len() > 0.9:
                
                if choose_mat < 0.8:
                    # diffuse
                    albedo = SolidColourTex(vec_mul(vec_rand(), vec_rand()))
                    sphere_material = Lambertian(albedo)
                    center2 = vec_add(center, V3(0, random.uniform(0, 0.5), 0))
                    world.add(MovingSphere(center, center2, 1.0, 0.2, 0.2, sphere_material))
                
                elif choose_mat < 0.95:
                    # metal
                    albedo = SolidColourTex(vec_rand_between(0.5, 1))
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                
                else:       
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    # Three big spheres
    material1 = Dielectric(1.5)
    world.add(Sphere(V3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(SolidColourTex(V3(0.4, 0.2, 0.1)))
    world.add(Sphere(V3(-4, 1, 0), 1.0, material2))

    material3 = Metal(SolidColourTex(V3(0.7, 0.6, 0.5)), 0.0)
    world.add(Sphere(V3(4, 1, 0), 1.0, material3))
    
    return world

def two_spheres() -> HittableList:
    world = HittableList()

    checker = CheckeredTex(SolidColourTex(V3(0.2, 0.3, 0.1)), SolidColourTex(V3(0.9, 0.9, 0.9)))

    world.add(Sphere(V3(0, -10, 0), 10, Lambertian(checker)))
    world.add(Sphere(V3(0, 10, 0), 10, Lambertian(checker)))

    return world


def two_perlin_spheres() -> HittableList:
    world = HittableList()

    pertext = NoiseTex(4)
    world.add(Sphere(V3(0, -1000, 0), 1000, Lambertian(pertext)))
    world.add(Sphere(V3(0, 2, 0), 2, Lambertian(pertext)))

    return world

def earth() -> HittableList:
    world = HittableList()

    earthtex = ImageTex("C:\\pdev\\PythonRaytrace\\textures\\earthmap.jpg")
    earthsurf = Lambertian(earthtex)

    earth = Sphere(V3(0, 0, 0), 2, earthsurf)

    world.add(earth)

    return world

def simple_light() -> HittableList:
    world = HittableList()

    pertext = NoiseTex(4)
    world.add(Sphere(V3(0, -1000, 0), 1000, Lambertian(pertext)))
    world.add(Sphere(V3(0, 2, 0), 2, Lambertian(pertext)))

    difflight = DiffuseLight(SolidColourTex(V3(4, 4, 4)))
    world.add(XYrect(3, 5, 1, 3, -2, difflight))

    return world

def cornell_box() -> HittableList:
    world = HittableList()

    red   = Lambertian(SolidColourTex(V3(0.65, 0.05, 0.05)))
    white = Lambertian(SolidColourTex(V3(0.73, 0.73, 0.73)))
    green = Lambertian(SolidColourTex(V3(0.12, 0.45, 0.15)))
    light = DiffuseLight(SolidColourTex(V3(15, 15, 15)))

    world.add(YZrect(0, 555, 0, 555, 555, green))
    world.add(YZrect(0, 555, 0, 555, 0, red))
    world.add(XZrect(213, 343, 227, 332, 554, light))
    world.add(XZrect(0, 555, 0, 555, 0, white))
    world.add(XZrect(0, 555, 0, 555, 555, white))
    world.add(XYrect(0, 555, 0, 555, 555, white))

    box1 = Box(V3(130, 0, 65), V3(295, 165, 230), white)
    box1 = RotateY(box1, 45)
    #box1 = Translate(box1, V3(260, 0, 295))    

    box2 = Box(V3(265, 0, 295), V3(430, 330, 460), white)
    box2 = RotateY(box2, 0)
    #box2 = Translate(box2, V3(130, 0, 65))

    world.add(box1)    
    world.add(box2)

    return world