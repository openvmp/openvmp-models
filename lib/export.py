def exportOBJ(model, filepath):
    vertices, triangles = model.tessellate(0.1)

    with open(filepath, "w") as f:
        f.write("# OBJ file\n")
        for v in vertices:
            f.write("v %.4f %.4f %.4f\n" % (v.x / 100.0, v.y / 100.0, v.z / 100.0))
        for p in triangles:
            f.write("f")
            for i in p:
                f.write(" %d" % (i + 1))
            f.write("\n")
