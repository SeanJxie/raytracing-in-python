from hittable_list import *
from geometry import *

def obj_to_world(fp: str) ->hittable_list:
    with open(fp, 'r') as f:
        lines = f.readlines()
    
    world = hittable_list()
    vertices = []

    for line in lines:
        slist = line.split()

        # Vertex
        if line.startswith('v '):
            vertices.append(vec3(float(slist[1]), float(slist[2]), float(slist[3])))
        
        # Face
        elif line.startswith('f '):
            rand_albedo = vec_mul(vec3.rand(), vec3.rand())
            rand_material = lambertian(rand_albedo)
            world.add(triangle(
                vertices[int(slist[1]) - 1], 
                vertices[int(slist[2]) - 1], 
                vertices[int(slist[3]) - 1], rand_material))

    return world
