
class Mesh:
    def __init__(self):
        self.positions = []
        self.normals = []
        self.uvs = []

def ply_header(num_verts):
    return f'''ply
format ascii 1.0
comment Created by micage
element vertex {num_verts}
property float x
property float y
property float z
property float s
property float t
property float nx
property float ny
property float nz
element face {int(num_verts/3)}
property list uchar uint vertex_indices
end_header
'''

def generate_normals(mesh):
    verts = mesh["verts"]
    tris = mesh["tris"]

    # generate triangle list, if not existing
    if not len(tris):
        num_tris, rest = divmod(len(verts))
        for i in range(num_tris):
            tris.append([i, i+1, i+2])
        mesh["tris"] = tris

    for i in len(verts):
        before = verts[:i]
        after = verts[i+1:]
        all = before + after # don't do this! better iterate them separately
        vert = verts[i]
        star = [] # all vertices at the same point in space
        for ii in range(len(all)):
            if all[ii] == vert:
                star.append()
        # find triangle, here we know the positions of the triangle
        # because they were generated
        conn_tris = map(lambda dup: tris[int(dup/3)], star) # generator of a 3-tuple of vertex indices
        # calculate face normals
        for tri in conn_tris:
            v1 = tri[0]
            v2 = tri[1]
            v3 = tri[2]

    return mesh

            

def save(file, mesh):
    verts = mesh["verts"]
    num_verts = len(verts)
    f = open(file, "w")

    f.write(ply_header(num_verts))

    for vert in verts:
        for val in vert:
            f.write(f"{val} ")
        f.write("\n")

    # generate face indices
    for face in range(int(num_verts/3)):
        f.write(f"3 {3*face} {3*face+1} {3*face+2}\n")

