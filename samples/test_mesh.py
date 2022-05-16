import math
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Mesh

def cross(v1, v2):
    x = v1[1]*v2[2] - v1[2]*v2[1]
    y = v1[2]*v2[0] - v1[0]*v2[2]
    z = v1[0]*v2[1] - v1[1]*v2[0]
    return [x, y, z]

def normal(v1, v2, v3):
    x,y,z = cross((v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]), (v1[0]-v3[0], v1[1]-v3[1], v1[2]-v3[2]))
    len = math.sqrt(x*x+y*y+z*z)
    return [x/len, y/len, z/len]

def sphere(radius, n_rho, n_phi):
    verts = []
    north = [0.0, 0.0, radius, 0.0, 0.0]
    south = [0.0, 0.0, -radius, 0.0, 0.0]
    grid = [[0 for _ in range(n_rho+1)] for _ in range(n_phi-1)]
    for j in range(n_phi-1):
        phi_phase = math.pi * (j+1)/n_phi
        z = math.cos(phi_phase)
        for i in range(n_rho):
            rho_phase = 2*math.pi * i/n_rho
            sin = math.sin(phi_phase)
            x = math.cos(rho_phase) * sin
            y = math.sin(rho_phase) * sin
            grid[j][i] = [radius * x, radius * y, radius * z, x, y]
        grid[j][n_rho] = grid[j][0] # copy first value so first equals last

    for i in range(n_rho):
        # connect 1st grid line with north, phi = 0
        tri = [ north, grid[0][i], grid[0][i+1] ]
        n = normal(*tri)
        north += n
        verts += tri

        # create 2 triangles, s = math.pi/n_phi, phi = range(s, (n_phi-2) * s, s)
        for j in range(n_phi-2):
            tri = [ grid[j][i  ], grid[j+1][i  ], grid[j  ][i+1] ]
            n = normal(*tri)
            for v in tri:
                v += n
            verts += tri
            tri = [ grid[j][i+1], grid[j+1][i  ], grid[j+1][i+1] ]
            n = normal(*tri)
            for v in tri:
                v += n
            verts += tri
        
        # connect last grid line with south, phi = (n_phi-1)/n_phi * math.pi
        tri = [ grid[n_phi-2][i+1], grid[n_phi-2][i], south ]
        n = normal(*tri)
        south += n
        verts += tri

    return { "verts": verts, "tris": [] }

mesh = sphere(10, 1<<4, 1<<3)
Mesh.save("assets/sphere20.ply", mesh)