import sys
import cadquery as cq
import cairosvg

sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts

if len(sys.argv) < 2:
    print("Usage: python3 " + sys.argv[0] + " <STEP-file>")
    sys.exit(1)

path = sys.argv[1]


def part_render(path):
    print("Rendering " + path + "...")
    bom = Bom()
    result = cq.Assembly()
    bom.add_part(result, path)

    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)
    # len = shape.BoundingBox().DiagonalLength
    xlen = shape.BoundingBox().xlen
    ylen = shape.BoundingBox().ylen
    zlen = shape.BoundingBox().zlen
    len = max(xlen, ylen, zlen)
    svgOpts = exportSvgOpts
    svgOpts["strokeWidth"] = len / 150.0

    print("Exporting " + path + " to STL...")
    shape.exportStl("generated_files/" + path + ".stl", 0.2, 1.0)

    print("Exporting " + path + " to SVG...")
    cq.exporters.export(
        shape,
        "generated_files/" + path + ".svg",
        opt=svgOpts,
    )
    print("Exporting " + path + " to PNG...")
    cairosvg.svg2png(
        url="generated_files/" + path + ".svg",
        write_to="generated_files/" + path + ".png",
        output_width=svgOpts["width"],
        output_height=svgOpts["height"],
    )


part_render(path)
