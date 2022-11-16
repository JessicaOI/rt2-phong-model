from lib import *
from math import *
from esfera import *
from material import *
from light import *
from intersect import *

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear_color = color(0,0,0)
        self.current_color = color(255,255,255)
        self.clear()
        self.scene = []
        self.background_color = color(0, 0, 0)
        self.light = Light(V3(0,0,0),1)

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def point(self,x,y,c=None):
        if y >= 0 and y < self.height and x >= 0 and x < self.width:
            self.framebuffer[y][x] = c or self.current_color
    
    def write(self, filename):
        write(filename, self.width, self.height, self.framebuffer)

    def render(self):
        fov = int(pi/2)
        ar = self.width/self.height
        tana = tan(fov/2)
        
        for y in range(self.height):
            for x in range(self.width):
                i = ((2 * (x + 0.5) / self.width) -1) * ar * tana
                j = ( (2 * (y + 0.5) / self.height)-1)* tana
                
                direction = norm(V3(i,j,-1))
                self.framebuffer[y][x] = self.cast_ray(V3(0,0,0), direction)
                

    def cast_ray(self,origin,direction):
         
        material, intersect = self.scene_intersect(origin, direction)

        if intersect is None:
            return self.background_color

        if material is None:
            return self.background_color
            

        light_dir = norm(sub(self.light.position, intersect.point))
        intensity = dot(light_dir, intersect.normal)

       
        light_reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (
        max(0, -dot(light_reflection, direction))**material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
        return diffuse + specular

    def scene_intersect(self,origin,direction):
        zbuffer = 999999
        material = None
        intersect = None

        for s in self.scene:
            object_intersect = s.ray_intersect(origin,direction)
            if object_intersect:
                if object_intersect.distance < zbuffer:
                    zbuffer = object_intersect.distance
                    material = s.material
                    intersect = object_intersect
        
        return material, intersect


# --------------------------------------------------
black = Material(diffuse=color(0, 0, 0), albedo=(0.3,  0.3), spec=3)
white = Material(diffuse=color(255, 255, 255), albedo=(0.9,  0.9), spec=35)
white2 = Material(diffuse=color(200, 200, 200), albedo=(1,  1), spec=20)
darkred = Material(diffuse=color(80,0,0), albedo=(0.6,  0.3), spec=50)
darkbrown = Material(diffuse=color(170, 80, 40), albedo=(0.9,  0.3), spec=7)
brown = Material(diffuse=color(230, 170, 135), albedo=(0.9,  0.9), spec=35)


r = Raytracer(800, 500)
r.light = Light(V3(7, 0, 10), 1.5)
r.scene = [
    #oso derecha

    #cabeza
    Esfera(V3(3, 0.85, -10), 1.4, brown),
    #cuerpo
    Esfera(V3(2.9, -2.1, -10), 1.8, darkred),
    #osico
    Esfera(V3(2.8, 0.5, -9), 0.49, darkbrown),
    #orejas
    Esfera(V3(3.9, 2, -9), 0.49, darkbrown),
    Esfera(V3(1.7, 2, -9), 0.49, darkbrown),
    #patas
    Esfera(V3(5, -1.2, -10), 0.66, brown),
    Esfera(V3(5, -3.5, -10), 0.66, brown),
    Esfera(V3(1, -1.2, -10), 0.66, brown),    
    Esfera(V3(1, -3.5, -10), 0.66, brown),
    #nariz
    Esfera(V3(2.5, 0.5, -8), 0.12, black),
    #ojos
    Esfera(V3(2.8, 1.1, -8), 0.2, black),
    Esfera(V3(2.2, 1.1, -8), 0.2, black),

    #oso izquierda

    #cabeza
    Esfera(V3(-3, 0.85, -10), 1.4, white),
    #cuerpo
    Esfera(V3(-2.9, -2.1, -10), 1.8, white2),
    #osico
    Esfera(V3(-2.8, 0.5, -9), 0.49, white),
    #orejas
    Esfera(V3(-3.9, 2, -9), 0.49, white),
    Esfera(V3(-1.7, 2, -9), 0.49, white),
    #patas
    Esfera(V3(-5, -1.2, -10), 0.66, white),
    Esfera(V3(-5, -3.5, -10), 0.66, white),
    Esfera(V3(-1, -1.2, -10), 0.66, white),    
    Esfera(V3(-1, -3.5, -10), 0.66, white),
    #nariz
    Esfera(V3(-2.5, 0.5, -8), 0.12, black),
    #ojos
    Esfera(V3(-2.8, 1.1, -8), 0.2, black),
    Esfera(V3(-2.2, 1.1, -8), 0.2, black),
]
