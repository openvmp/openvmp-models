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
result = cq.Assembly(name="camera_servo_link")

servo_attachment, servo_attachment_name = bom.get_part(
    "parts/gobilda/motion-servo-attach-hub-low-25t"
)
servo_mount, servo_mount_name = bom.get_part(
    "parts/gobilda/structure-mount-servo-43mm-std"
)
servo_hs488hb, servo_hs488hb_name = bom.get_part("parts/gobilda/motion-servo-hs-488hb")

#   - servo attachment
result.add(
    servo_attachment,
    name=servo_attachment_name,
    loc=cq.Location((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), 90),
)
#   - servo mount
result.add(
    servo_mount,
    name=servo_mount_name,
    loc=cq.Location((6.75, -17.0, 8.875), (0.0, 0.0, 1.0), -90),
)
#   - servo
result.add(
    servo_hs488hb,
    name=servo_hs488hb_name,
    loc=cq.Location((32.75, 14.0, 34.375), (0.0, 0.0, 1.0), 90),
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
        models + "/../platform/src/openvmp_robot_don1/meshes/camera_servo.stl", 0.5, 5.0
    )
    print("Generating OBJ...")
    exportOBJ(
        shape, models + "/../platform/src/openvmp_robot_don1/meshes/camera_servo.obj"
    )

    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        models + "/generated_files/robots/don1/camera_servo.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url=models + "/generated_files/robots/don1/camera_servo.svg",
        write_to=models + "/generated_files/robots/don1/camera_servo.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "camera_servo_link",
        },
    )
