import Mesh
import math

mesh = {
    "verts": [],
    "tris": []
}

def spherical(r, rho, phi):
    return [
        r * math.cos(2*math.pi*rho) * math.sin(),
        r * math.sin(2*math.pi*rho),
    ]

def generate_sphere(radius):
    verts = []
    north = (0, 0, radius)
    south = (0, 0, -radius)
    grid = [[0 for _ in range(16+1)] for _ in range(6)]
    for j in range(6):
        phi_phase = math.pi * (j+1)/8
        z = radius * math.cos(phi_phase)
        for i in range(16):
            phase = 2*math.pi*i/16
            sin = math.sin(phi_phase)
            x = radius * math.cos(phase) * sin
            y = radius * math.sin(phase) * sin
            grid[j][i] = (x,y,z)
        grid[j][16] = grid[j][0] # copy first value so first equals last

    # connect 1st grid line with north 
    for i in range(16):
        verts.append([
            north, grid[i], grid[i+1]
        ])
    # create 2 triangles
    for j in range(6):
        for i in range(16):
            verts.append()
    # connect 2nd grid line with south



