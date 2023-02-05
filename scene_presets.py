import random

from hittablelist import *
from material import *
from vec import *
from camera import *

from sphere import *
from aarect import *
from box import *
from constantmedium import *
from bvh import *

random.seed(1234)

def scattered_spheres() -> tuple[HittableList, Camera]:
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
    
    return world, None

def two_spheres() -> tuple[HittableList, Camera]:
    world = HittableList()

    checker = CheckeredTex(SolidColourTex(V3(0.2, 0.3, 0.1)), SolidColourTex(V3(0.9, 0.9, 0.9)))

    world.add(Sphere(V3(0, -10, 0), 10, Lambertian(checker)))
    world.add(Sphere(V3(0, 10, 0), 10, Lambertian(checker)))

    return world


def two_perlin_spheres() -> tuple[HittableList, Camera]:
    world = HittableList()

    pertext = NoiseTex(4)
    world.add(Sphere(V3(0, -1000, 0), 1000, Lambertian(pertext)))
    world.add(Sphere(V3(0, 2, 0), 2, Lambertian(pertext)))

    return world, None

def earth() -> tuple[HittableList, Camera]:
    world = HittableList()

    earthtex = ImageTex(".\\textures\\earthmap.jpg")
    earthsurf = Lambertian(earthtex)

    earth = Sphere(V3(0, 0, 0), 2, earthsurf)

    world.add(earth)

    return world, None

def simple_light() -> tuple[HittableList, Camera]:
    world = HittableList()

    pertext = NoiseTex(4)
    world.add(Sphere(V3(0, -1000, 0), 1000, Lambertian(pertext)))
    world.add(Sphere(V3(0, 2, 0), 2, Lambertian(pertext)))

    difflight = DiffuseLight(SolidColourTex(V3(4, 4, 4)))
    world.add(XYrect(3, 5, 1, 3, -2, difflight))

    return world, None

def cornell_box() -> tuple[HittableList, Camera]:
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

    # Tall
    box1 = Box(V3(0, 0, 0), V3(165, 330, 165), white)
    box1 = RotateY(box1, 15)
    box1 = Translate(box1, V3(260, 0, 295))    

    # Short
    box2 = Box(V3(0, 0, 0), V3(165, 165, 165), white)
    box2 = RotateY(box2, -18)
    box2 = Translate(box2, V3(130, 0, 65))

    world.add(box1)    
    world.add(box2)

    lookat = V3(278, 278, 0)
    lookfrom = V3(278, 278, -800)
    cam = Camera(lookfrom, lookat, V3(0, 1, 0), 40, 1, 0.0, vec_sub(lookat, lookfrom).len(), 0, 1)

    return world, cam

def cornell_box_smoke() -> tuple[HittableList, Camera]:
    world = HittableList()

    red   = Lambertian(SolidColourTex(V3(0.65, 0.05, 0.05)))
    white = Lambertian(SolidColourTex(V3(0.73, 0.73, 0.73)))
    green = Lambertian(SolidColourTex(V3(0.12, 0.45, 0.15)))
    light = DiffuseLight(SolidColourTex(V3(15, 15, 15)))

    world.add(YZrect(0, 555, 0, 555, 555, green))
    world.add(YZrect(0, 555, 0, 555, 0, red))
    world.add(XZrect(113, 443, 127, 432, 554, light))
    world.add(XZrect(0, 555, 0, 555, 0, white))
    world.add(XZrect(0, 555, 0, 555, 555, white))
    world.add(XYrect(0, 555, 0, 555, 555, white))

    # Tall
    box1 = Box(V3(0, 0, 0), V3(165, 330, 165), white)
    box1 = RotateY(box1, 15)
    box1 = Translate(box1, V3(260, 0, 295))    

    # Short
    box2 = Box(V3(0, 0, 0), V3(165, 165, 165), white)
    box2 = RotateY(box2, -18)
    box2 = Translate(box2, V3(130, 0, 65))

    world.add(ConstantMedium(box1, 0.01, SolidColourTex(V3(0, 0, 0))))    
    world.add(ConstantMedium(box2, 0.01, SolidColourTex(V3(1, 1, 1))))    

    lookat = V3(278, 278, 0)
    lookfrom = V3(278, 278, -800)
    cam = Camera(lookfrom, lookat, V3(0, 1, 0), 40, 1, 0.0, vec_sub(lookat, lookfrom).len(), 0, 1)

    return world, cam

def artwork() -> tuple[HittableList, Camera]:
    boxes1 = HittableList()
    ground = Lambertian(SolidColourTex(V3(0.48, 0.83, 0.53)))
    world = HittableList()
    boxes_per_side = 20
    for i in range(boxes_per_side):
        for j in range(boxes_per_side):
            w = 100
            x0 = -1000 + i * w
            z0 = -1000 + j * w
            y0 = 0
            x1 = x0 + w
            y1 = random.uniform(1, 101)
            z1 = z0 + w

            boxes1.add(Box(V3(x0, y0, z0), V3(x1, y1, z1), ground))

    
    world.add(BVHnode(boxes1, 0, len(boxes1.objects), 0, 1))

    light = DiffuseLight(SolidColourTex(V3(7, 7, 7)))
    world.add(XZrect(123, 423, 147, 412, 554, light))

    center1 = V3(400, 400, 200);
    center2 = vec_add(center1, V3(30,0,0))
    moving_sphere_material = Lambertian(SolidColourTex(V3(0.7, 0.3, 0.1)))

    world.add(MovingSphere(center1, center2, 0, 1, 50, moving_sphere_material))
    world.add(Sphere(V3(260, 150, 45), 50, Dielectric(1.5)))
    world.add(Sphere(V3(0, 150, 145), 50, Metal(SolidColourTex(V3(0.8, 0.8, 0.9)), 1.0)))

    boundary = Sphere(V3(360, 150, 145), 70, Dielectric(1.5))
    world.add(boundary)
    world.add(ConstantMedium(boundary, 0.2, SolidColourTex(V3(0.2, 0.4, 0.9))))
    boundary = Sphere(V3(0, 0, 0), 5000, Dielectric(1.5))
    world.add(ConstantMedium(boundary, 0.0001, SolidColourTex(V3(1, 1, 1))))

    emat = Lambertian(ImageTex(".\\textures\\earthmap.jpg"))
    world.add(Sphere(V3(400, 200, 400), 100, emat))
    pertext = NoiseTex(0.1)
    world.add(Sphere(V3(220, 280, 300), 80, Lambertian(pertext)))

    boxes2 = HittableList()
    white = Lambertian(SolidColourTex(V3(.73, .73, .73)))
    ns = 1000
    for j in range(ns):
        boxes2.add(Sphere(vec_rand_between(0,165), 10, white))

    world.add(Translate(
        RotateY(
            BVHnode(boxes2, 0, len(boxes2.objects), 0.0, 1.0), 15),
            V3(-100, 270, 395)
        )
    )

    lookat = V3(278, 278, 0)
    lookfrom = V3(478, 278, -600)
    cam = Camera(lookfrom, lookat, V3(0, 1, 0), 40, 1, 0.0, vec_sub(lookat, lookfrom).len(), 0, 1)

    return world, cam