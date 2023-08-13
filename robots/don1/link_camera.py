if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import ocp_vscode as ov
import cadquery as cq

import cairosvg
import sys

sys.path.append("models")
sys.path.append("..")
sys.path.append(".")
sys.path.append("models")
from lib.bom import Bom
from lib.doc import exportSvgOpts
from lib.export import exportOBJ
from lib.common import get_models_dir


models = get_models_dir()
bom = Bom()
result = cq.Assembly(name="camera_link")

servo_arm_attachment, servo_arm_attachment_name = bom.get_part(
    "parts/gobilda/motion-servo-attach-arm-25t"
)
camera_channel, camera_channel_name = bom.get_part(
    "parts/gobilda/structure-u-channel-low-3"
)

#   - servo arm attachment
result.add(
    servo_arm_attachment,
    name=servo_arm_attachment_name,
    loc=cq.Location((2.0, 0.0, 0.0), (0.58, 0.58, -0.58), 240),
)
#   - camera channel
result.add(
    camera_channel,
    name=camera_channel_name,
    loc=cq.Location((48.0, -24.5, 21.5), (0.0, 0.0, 1.0), 90),
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
        models + "/../platform/src/openvmp_robot_don1/meshes/camera.stl", 0.5, 5.0
    )
    print("Generating OBJ...")
    exportOBJ(shape, models + "/../platform/src/openvmp_robot_don1/meshes/camera.obj")

    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        models + "/generated_files/robots/don1/camera.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url=models + "/generated_files/robots/don1/camera.svg",
        write_to=models + "/generated_files/robots/don1/camera.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "camera_link",
        },
    )
