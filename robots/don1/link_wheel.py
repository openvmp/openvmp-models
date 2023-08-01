if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq

import cairosvg
import sys

sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts


result = cq.Assembly(name="wheel_link")
bom = Bom()

wheel, wheel_name = bom.get_part("./parts/dfrobot/rubber-wheel")
result.add(
    wheel,
    name=wheel_name,
    loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
)

if __name__ == "__main__":
    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating STL...")
    shape.exportStl("../platform/src/openvmp_robot_don1/meshes/wheel.stl", 0.5, 5.0)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        "generated_files/robots/don1/wheel.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url="generated_files/robots/don1/wheel.svg",
        write_to="generated_files/robots/don1/wheel.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "wheel_link",
        },
    )
