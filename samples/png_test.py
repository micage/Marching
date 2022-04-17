import png
from perlin_noise import PerlinNoise

Array2d = lambda row, col, gen: [[gen(row, col, 0)] * col for _ in range(row)]

noise3 = PerlinNoise(octaves=3, seed=775)
noise6 = PerlinNoise(octaves=6, seed=776)
noise12 = PerlinNoise(octaves=12, seed=777)
noise24 = PerlinNoise(octaves=24, seed=778)

nx = 1<<8
ny = 1<<8

def noise(x,y,z):
    return     noise3([x,y,z]) + \
        .5 *   noise6([x,y,z]) + \
        .25 *  noise12([x,y,z]) + \
        .125 * noise24([x,y,z])

img = [[int(128*(noise(row/nx, col/ny, 0)+1)) for row in range(nx)] for col in range(ny)]

f = open('assets/noise.png', 'wb')
w = png.Writer(nx, ny, greyscale=True)
w.write(f, img)
f.close()


# p = [(255,0,0, 0,255,0, 0,0,255),
#      (128,0,0, 0,128,0, 0,0,128)]
# f = open('swatch.png', 'wb')
# w = png.Writer(3, 2, greyscale=False)
# w.write(f, p)
# f.close()