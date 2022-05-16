import numpy as np

rng = np.random.default_rng(12345)
# rints = rng.integers(low=0, high=10, size=3)
# print(rints)
rfloats = rng.random(size=3)
print(rfloats)

nx, ny = 1<<3, (1<<3)

f = open("assets/noise.ply", "w")
f.write(f'''ply
format ascii 1.0
comment Created by micage
element vertex {ny*3}
property float x
property float y
property float z
property float nx
property float ny
property float nz
property float s
property float t
element face {ny}
property list uchar uint vertex_indices
end_header
''')
def vertex():
    return [

    ]

a = [rng.random(size=8)*2-1 for _ in range(ny*3)]

for line in a:
    for val in line:
        f.write(f"{val} ")
    f.write("\n")

for face in range(ny):
    f.write(f"3 {3*face} {3*face+1} {3*face+2}\n")

f.close()