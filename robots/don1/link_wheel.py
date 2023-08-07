if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import ocp_vscode as ov
import cadquery as cq

import cairosvg
import sys

sys.path.append("models")
sys.path.append("..")
sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts
from lib.common import get_models_dir


models = get_models_dir()
bom = Bom()
result = cq.Assembly(name="wheel_link")

wheel, wheel_name = bom.get_part("parts/dfrobot/rubber-wheel")
result.add(
    wheel,
    name=wheel_name,
    loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
)

if __name__ == "__main__":
    shape = result.toCompound()

    try:
        ov.config.status()
        print("Visualizing...")
        ov.show(shape)
    except:
        print('No VS Code or "OCP CAD Viewer" extension detected.')

    print("Generating STL...")
    shape.exportStl(
        models + "/../platform/src/openvmp_robot_don1/meshes/wheel.stl", 0.5, 5.0
    )

    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        models + "/generated_files/robots/don1/wheel.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url=models + "/generated_files/robots/don1/wheel.svg",
        write_to=models + "/generated_files/robots/don1/wheel.png",
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
