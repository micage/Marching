from math import sin, cos, pi, sqrt
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Mesh
import itertools

# (a + b) / a = a / b   "Golden Ratio"
# with a = 1 => b = (√5 - 1)/2
# so Φ = a + b = 1 + b = (1 + √5)/2

# vertex coordinates, 3 plane form
# (0, ±1, ±Φ)
# (±1, ±Φ, 0)
# (±Φ, 0, ±1)

# => radius R = sqrt(Φ^2 + 1), half of a plane diagonal

def normal(a,b,c):
    vx, vy, vz = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    wx, wy, wz = c[0] - b[0], c[1] - b[1], c[2] - b[2]
    s = sqrt(1/3) # this is special for a unit icosahedron
    # nx, ny, nz = vy * wz - vz * wy, vz * wx - vx * wz, vx * wy - vy * wx
    # d = 1/sqrt(nx*nx + ny*ny + nz*nz)
    return [
        (vy * wz - vz * wy) * s,
        (vz * wx - vx * wz) * s,
        (vx * wy - vy * wx) * s
    ]

Y = (1 + sqrt(5))/2
Φ = Y - 1 

# "Golden Rectangles"
green = [[-Y, 1, 0], [-Y, -1,  0], [ Y, -1,  0], [ Y,  1,  0]] * 5
red =   [[-1, 0, Y], [ 1,  0,  Y], [ 1,  0, -Y], [-1,  0, -Y]] * 5
blue =  [[ 0, Y, 1], [ 0,  Y, -1], [ 0, -Y, -1], [ 0, -Y,  1]] * 5

positions = [
    # connect 2 green with 1 red
    green[0    ], green[1    ], red[0], 
    green[1 + 4], green[0 + 4], red[3],
    green[2    ], green[3    ], red[1],
    green[3 + 4], green[2 + 4], red[2],

    # connect 2 red with one blue
    red[0 + 1 * 4], red[1 + 1 * 4], blue[0],
    red[1 + 2 * 4], red[0 + 2 * 4], blue[3],
    red[2 + 1 * 4], red[3 + 1 * 4], blue[1],
    red[3 + 2 * 4], red[2 + 2 * 4], blue[2],

    # connect 2 blue with one green
    blue[0 + 1 * 4], blue[1 + 1 * 4], green[0 + 2 * 4],
    blue[1 + 2 * 4], blue[0 + 2 * 4], green[3 + 2 * 4],
    blue[2 + 1 * 4], blue[3 + 1 * 4], green[1 + 2 * 4],
    blue[3 + 2 * 4], blue[2 + 2 * 4], green[2 + 2 * 4],

    # connect 1 green, 1 red, 1 blue
    green[0 + 3 * 4],  red[0 + 3 * 4], blue[0 + 3 * 4],
    green[1 + 3 * 4], blue[3 + 3 * 4],  red[0 + 4 * 4],
    green[2 + 3 * 4],  red[1 + 3 * 4], blue[3 + 4 * 4],
    green[3 + 3 * 4], blue[0 + 4 * 4],  red[1 + 4 * 4],

    green[0 + 4 * 4], blue[1 + 3 * 4],  red[3 + 3 * 4],
    green[1 + 4 * 4],  red[3 + 4 * 4], blue[2 + 3 * 4],
    green[2 + 4 * 4], blue[2 + 4 * 4],  red[2 + 3 * 4],
    green[3 + 4 * 4],  red[2 + 4 * 4], blue[1 + 4 * 4]
]

s = sqrt(1/3)
M, N = Y * s, (Y-1) * s
normals = [
    [[-M, 0, -N]] * 3, 
    [[-M, 0,  N]] * 3, 
    [[ M, 0,  N]] * 3, 
    [[ M, 0, -N]] * 3,

    [[0, -N,  M]] * 3,
    [[0,  N,  M]] * 3,
    [[0,  N, -M]] * 3,
    [[0, -N, -M]] * 3,

    [[ N,  M, 0]] * 3,
    [[-N,  M, 0]] * 3,
    [[-N, -M, 0]] * 3,
    [[ N, -M, 0]] * 3,
    
    [[ -s,  s,  s]] * 3,
    [[ -s, -s,  s]] * 3,
    [[  s, -s,  s]] * 3,
    [[  s,  s,  s]] * 3,
    
    [[ -s,  s, -s]] * 3,
    [[ -s, -s, -s]] * 3,
    [[  s, -s, -s]] * 3,
    [[  s,  s, -s]] * 3,
]
normals = list(itertools.chain.from_iterable(normals))

uvs = [ [0, 0], [sqrt(.75), 0.5], [1, 0] ] * 20 # dummy list

tris = [*range(60)] # trivial vertex list

verts = [[*(positions[i]), *(uvs[i]), *(normals[i])] for i in range(60)]

def create():
    return {
        "verts": verts, "tris": tris
    }

Mesh.save("assets/icosa_1.ply", create())