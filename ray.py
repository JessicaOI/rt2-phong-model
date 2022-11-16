from lib import *
from math import *
from esfera import *
from material import *

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear_color = color(0,0,0)
        self.current_color = color(255,255,255)
        self.clear()
        self.scene = []
        self.background_color = color(0, 0, 0)

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
                j = (1 - (2 * (y + 0.5) / self.height))* tana
                
                direction = norm(V3(i,j,-1))
                self.framebuffer[y][x] = self.cast_ray(V3(0,0,0), direction)
                

    def cast_ray(self,origin,direction):
        material = self.scene_intersect(origin, direction)
        if material:
            return material.diffuse
        else:
            return self.background_color

    def scene_intersect(self,origin,direction):
        for s in self.scene:
            if s.ray_intersect(origin, direction):
                return s.material
        return None


# ------------------------------------------------------

white = Material(diffuse=color(255, 255, 255))
black = Material(diffuse=color(0, 0, 0))
orange = Material(diffuse=color(255, 165, 0))
brown = Material(diffuse=color(63,32,6))
red = Material(diffuse=color(255,0,0))

r = Raytracer(800, 600)
r.scene = [

    #nariz y ojos
    Esfera(V3(0, -2.5,-10), 0.3, orange),

    Esfera(V3(0.5, -3,-10), 0.1, black),
    Esfera(V3(-0.5, -3,-10), 0.1, black),
    Esfera(V3(0.5, -3,-10), 0.2, white),
    Esfera(V3(-0.5, -3,-10), 0.2, white),

    #sonrisa
    Esfera(V3(-0.6, -2.1,-10), 0.09, black),
    Esfera(V3(-0.3, -1.9,-10), 0.09, black),
    Esfera(V3(0, -1.9,-10), 0.09, black),
    Esfera(V3(0.3, -1.9,-10), 0.09, black),
    Esfera(V3(0.6, -2.1,-10), 0.09, black),

    #corbata
    Esfera(V3(-0.5, -1.4,-10), 0.25, red),
    Esfera(V3(0.5, -1.4,-10), 0.25, red),
    Esfera(V3(0, -1.4,-10), 0.25, red),
    Esfera(V3(0, -0.9,-10), 0.25, red),
    Esfera(V3(0, -0.4,-10), 0.25, red),

    #bolas de nieve
    Esfera(V3(0, -2.4,-10), 1.2, white),
    Esfera(V3(0, 0,-10), 1.8, white),
    Esfera(V3(0, 4,-12), 2.5, white),


    #brazos

    #izquierdo
    Esfera(V3(-1.8, -0.4,-10), 0.11, brown),
    Esfera(V3(-1.9, -.5,-10), 0.11, brown),
    Esfera(V3(-2, -0.6,-10), 0.11, brown),
    Esfera(V3(-2.1, -0.7,-10), 0.11, brown),
    Esfera(V3(-2.2, -0.8,-10), 0.11, brown),
    Esfera(V3(-2.3, -0.9,-10), 0.11, brown),
    Esfera(V3(-2.4, -1,-10), 0.11, brown),
    Esfera(V3(-2.5, -1.1,-10), 0.11, brown),
    Esfera(V3(-2.69, -1.,-10), 0.11, brown),
    Esfera(V3(-2.8, -1.,-10), 0.11, brown),
    Esfera(V3(-2.99, -1.,-10), 0.11, brown),
    Esfera(V3(-3.1, -1.,-10), 0.11, brown),
    Esfera(V3(-3.29, -1.,-10), 0.11, brown),

    Esfera(V3(-2.69, -2,-10), 0.11, brown),
    Esfera(V3(-2.65, -1.8,-10), 0.11, brown),
    Esfera(V3(-2.60, -1.6,-10), 0.11, brown),
    Esfera(V3(-2.55, -1.4,-10), 0.11, brown),
    Esfera(V3(-2.5, -1.2, -10), 0.11, brown),
    
    #derecho
    Esfera(V3(1.8, -0.4,-10), 0.11, brown),
    Esfera(V3(1.9, -0.5,-10), 0.11, brown),
    Esfera(V3(2, -0.6,-10), 0.11, brown),
    Esfera(V3(2.1, -0.7,-10), 0.11, brown),
    Esfera(V3(2.2, -0.8,-10), 0.11, brown),
    Esfera(V3(2.3, -0.9,-10), 0.11, brown),
    Esfera(V3(2.4, -1,-10), 0.11, brown),
    Esfera(V3(2.5, -1.1,-10), 0.11, brown),
    Esfera(V3(2.69, -1,-10), 0.11, brown),
    Esfera(V3(2.8, -1,-10), 0.11, brown),
    Esfera(V3(2.99, -1,-10), 0.11, brown),
    Esfera(V3(3.1, -1,-10), 0.11, brown),
    Esfera(V3(3.29, -1,-10), 0.11, brown),

    Esfera(V3(2.69, -2,-10), 0.11, brown),
    Esfera(V3(2.65, -1.8,-10), 0.11, brown),
    Esfera(V3(2.60, -1.6,-10), 0.11, brown),
    Esfera(V3(2.55, -1.4,-10), 0.11, brown),
    Esfera(V3(2.5, -1.2, -10), 0.11, brown),
    
]
