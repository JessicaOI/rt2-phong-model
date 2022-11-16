import struct
import random
import math
from collections import namedtuple

#vectores
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])
# 1 byte
def char(c):
    return struct.pack('=c', c.encode('ascii'))

# 2 bytes
def word(c):
    return struct.pack('=h', c)

# 4 bytes 
def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

# Coordenadas Baricentricas
def barycentric(A, B, C, P):
    bary = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x), 
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if abs(bary[2]) < 1:
        return -1, -1, -1  

    return (
        1 - (bary[0] + bary[1]) / bary[2], 
        bary[1] / bary[2], 
        bary[0] / bary[2]
    )


def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

# producto punto
def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

# producto cruz
def cross(v0, v1):
    return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
)

def multi(v0,k):
    return V3(
        v0.x * k,
        v0.y * k,
        v0.z * k
    )

# largo del vector
def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices): 
    xs = [ vertex.x for vertex in vertices ]
    ys = [ vertex.y for vertex in vertices ]
    xs.sort()
    ys.sort()

    return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])

def suma(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def write(filename, width, height, framebuffer):
    f = open(filename, 'bw')

    # pixel header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + width * height * 3))
    f.write(word(0))
    f.write(word(0))
    f.write(dword(14 + 40))

    # info header
    f.write(dword(40))
    f.write(dword(width))
    f.write(dword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(width * height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # pixel data
    for x in range(height):
        for y in range(width):
            f.write(framebuffer[x][y])

    f.close()