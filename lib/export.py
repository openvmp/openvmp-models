# For details, see: https://en.wikipedia.org/wiki/Wavefront_.obj_file


def exportOBJ(model, filepath):
    try:
        vertices, triangles = model.tessellate(0.5)

        with open(filepath, "w") as f:
            f.write("# OBJ file\n")
            for v in vertices:
                f.write("v %.4f %.4f %.4f\n" % (v.x, v.y, v.z))
            for p in triangles:
                f.write("f")
                for i in p:
                    f.write(" %d" % (i + 1))
                f.write("\n")
    except:
        print("Exception while exporting to " + filepath)
