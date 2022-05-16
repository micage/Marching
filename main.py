from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import png
import math
# f = lambda x,y,z:  math.sqrt(x**2 + y**2 + z**2)
import Tables
import Mesh

# options
FILE_NAME = "assets/noise_4.ply"
surfaceLevel = .0 # isosurface value
safe_values = 0
safe_configs = 0
show_plot = 0
grid_density = 5

nx = 1<<grid_density
ny = 1<<grid_density
nz = 1<<grid_density

makeArray2d = lambda row, col: [[0] * col for _ in range(row)]
makeArray3d = lambda x, y, z: [[[0 for _ in range(x)] for _ in range(y)] for _ in range(z)]
# makeArray3d = lambda x, y, z: { (i,j,k):0 for i in range(x) for j in range(y) for j in range(z) }

def save_png(to_file, img, width, height):
    f = open(to_file, 'wb')
    w = png.Writer(width, height, greyscale=True)
    w.write(f, img)
    f.close()

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def clebsch(x,y,z):
    return 81*(x**3 + y**3 + z**3) \
        - 189*(x**2*y + x**2*z + y**2*x \
        + y**2*z + z**2*x + z**2*y) \
        + 54*(x*y*z) \
        + 126*(x*y + x*z + y*z) \
        - 9*(x**2 + y**2 + z**2) \
        - 9*(x + y + z) + 1


def metaball(x,y,z):
    return   2 / ((x-(-2.5))**2 + (y-( 0))**2 + (z-.001)**2) \
          + -3 / ((x      )**2 + (y-( 0))**2 + (z-.001)**2) \
          +  5 / ((x-( 2))**2 + (y-( 0))**2 + (z-.001)**2) - .2 \
          -  2 / ((x-( 3))**2 + (y-( 0))**2 + (z-.001)**2) - .2

noise3 = PerlinNoise(octaves=3, seed=775)
noise6 = PerlinNoise(octaves=6, seed=776)
noise12 = PerlinNoise(octaves=12, seed=777)
noise24 = PerlinNoise(octaves=24, seed=778)

def noise(x,y,z):
    return     noise3([x,y,z]) + \
        .5 *   noise6([x,y,z]) + \
        .25 *  noise12([x,y,z]) + \
        .125 * noise24([x,y,z])

def noise2(x,y,z):
    return noise(x/nx, y/ny, z/nz) / (z+1) + 0.05 
 
# create a 3d grid of noise values -> scalar field
# values = [[ [noise(x/nx, y/ny, z/nz) for x in range(nx+1)] for y in range(ny+1)] for z in range(nz+1)]
# values = [[ [cubic1(x/nx, y/ny, z/nz) for x in range(nx+1)] for y in range(ny+1)] for z in range(nz+1)]
# values = [[ [metaball(10.0 * (x/nx-.5), 10.0 * (y/ny-.5), 10.0 * (z/nz-.5)) for x in range(nx+1)] for y in range(ny+1)] for z in range(nz+1)]
values = [[ [clebsch(10.0 * (x/nx-.5), 10.0 * (y/ny-.5), 10.0 * (z/nz-.5)) for x in range(nx+1)] for y in range(ny+1)] for z in range(nz+1)]
# values = [[[noise2(x,y,z) for x in range(nx+1)] for y in range(ny+1)] for z in range(nz+1)]



if(safe_values):
    for i in range(len(values)):
        img = [[int(128*(values[i][y][x] + 1)) for x in range(nx)] for y in range(ny)]
        save_png(f"assets/noise1/noise1_{i}.png", img, nx, ny)

mesh = { "verts": [], "tris": [] }

if(safe_configs):
    configs = makeArray3d(nx,ny,nz)

for i in range(nz):
    for j in range(ny):
        for k in range(nx):
            cube = [
                values[i  ][j][k], values[i  ][j][k+1], values[i  ][j+1][k+1], values[i  ][j+1][k], 
                values[i+1][j][k], values[i+1][j][k+1], values[i+1][j+1][k+1], values[i+1][j+1][k]
            ] # 8 "marching" vertices

            # load or generate cube configuration
            cubeConfig = 0
            for n in range(8):
                if(cube[n] < surfaceLevel):
                    cubeConfig |= 1 << n
            
            if(safe_configs):
                configs[i][j][k] = cubeConfig

            edges = Tables.triangles[cubeConfig]
            edge_index = 0
            grid_point = [k,j,i]

            while (edges[edge_index] != -1):
                tri = []
                for ii in range(3):
                    edge = edges[edge_index + ii]       # tuple of 2 vertex indices

                    vert_a_i = Tables.edges2[edge][0]   # vertex index 0
                    vert_b_i = Tables.edges2[edge][1]   # vertex index 1
                    vert_a_val = cube[vert_a_i]         # value at vertex a
                    vert_b_val = cube[vert_b_i]         # value at vertex b

                    # interpolate w.r.t. values of vert_a and vert_b
                    s = (surfaceLevel - vert_a_val)/(vert_b_val - vert_a_val)  # interpolation factor

                    # tri.append([
                    #     *map(lambda v1, v2, v3: (1-s) * v1 + s * v2 + v3, 
                    #             Tables.corners[vert_a_i], 
                    #             Tables.corners[vert_b_i], 
                    #             grid_point
                    #     )
                    # ])

                    # # append missing normal and uv coordinates, it's a cheap hack
                    # mesh["verts"].append(tri[ii]+[0,0,1, 0,0])
                    pos = []
                    for jj in range(3):
                        pos.append((1-s) * Tables.corners[vert_a_i][jj] + s * Tables.corners[vert_b_i][jj] + grid_point[jj])
                    
                    mesh["verts"].append(pos + [0,0,1, 0,0])

                edge_index += 3
    if(safe_configs):
        save_png(f"assets/config1/config1_{i}.png", configs[i], nx, ny)

# test reading the files into arrays again, does not work :(
# read_noise1 = []
# for i in range(nz+1):
#     f = open(f"assets/noise1/noise1_{i}.png","rb")
#     r = png.Reader(f)
#     w, h, pixels, meta = r.read()
#     # TODO transcode pixels into its original form
#     read_noise1.append(pixels)

# save mesh, only "verts" are present
Mesh.save(FILE_NAME, mesh)

# matplotlib outputs
if (show_plot):
    f, axarr = plt.subplots(8,2) 
    axarr[0][0].imshow(values[0], cmap='gray')
    axarr[0][1].imshow(configs[0], cmap='summer')

    axarr[1][0].imshow(values[1], cmap='gray')
    axarr[1][1].imshow(configs[1], cmap='summer')

    axarr[2][0].imshow(values[2], cmap='gray')
    axarr[2][1].imshow(configs[2], cmap='summer')

    axarr[3][0].imshow(values[3], cmap='gray')
    axarr[3][1].imshow(configs[3], cmap='summer')

    axarr[4][0].imshow(values[4], cmap='gray')
    axarr[4][1].imshow(configs[4], cmap='summer')

    axarr[5][0].imshow(values[5], cmap='gray')
    axarr[5][1].imshow(configs[5], cmap='summer')

    axarr[6][0].imshow(values[6], cmap='gray')
    axarr[6][1].imshow(configs[6], cmap='summer')

    axarr[7][0].imshow(values[7], cmap='gray')
    axarr[7][1].imshow(configs[7], cmap='summer')

    plt.show()

