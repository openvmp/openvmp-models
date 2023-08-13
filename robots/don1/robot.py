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
result = cq.Assembly()

# Link: base_link
base, base_name = bom.get_assembly("robots/don1/link_base.py")
result.add(base, name=base_name)

for half, dir in [("front", 1), ("rear", -1)]:
    half_assembly = cq.Assembly()
    # Link: <half>_turn_table_link
    turn_table_link, _ = bom.get_assembly("robots/don1/link_turn_table.py")
    half_assembly.add(
        turn_table_link,
        name=half + "_turn_table_link",
        loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
    )

    hip_assembly = cq.Assembly()
    # Link: <half>_hip_link
    hip_link, _ = bom.get_assembly("robots/don1/link_hip.py")
    hip_assembly.add(
        hip_link,
        name=half + "_hip_link",
        loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
    )

    for side, side_dir in [("left", 1), ("right", -1)]:
        side_assembly = cq.Assembly()

        # Link: <half>_<side>_camera_servo_link
        camera_servo_link, _ = bom.get_assembly("robots/don1/link_camera_servo.py")
        if dir == 1:
            camera_servo_link = camera_servo_link.mirror(mirrorPlane="XZ")
        if dir * side_dir == -1:
            camera_servo_link = camera_servo_link.mirror(mirrorPlane="YZ")

        camera_servo_assembly = cq.Assembly()
        camera_servo_assembly.add(
            camera_servo_link,
            loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
        )

        # Link: <half>_<side>_camera_link
        camera_link, _ = bom.get_assembly("robots/don1/link_camera.py")
        if dir == 1:
            camera_link = camera_link.mirror(mirrorPlane="XZ")
        if dir * side_dir == 1:
            camera_link = camera_link.mirror(mirrorPlane="YZ")

        camera_servo_assembly.add(
            camera_link,
            name=half + "_" + side + "_camera_link",
            loc=cq.Location(
                (-dir * side_dir * 13.0, -dir * 4.0, 24.5), (0.0, 0.0, 1.0), 0
            ),
        )

        side_assembly.add(
            camera_servo_assembly,
            name=half + "_" + side + "_camera_servo_link",
            loc=cq.Location(
                (
                    side_dir * (122.5 - 90.0),
                    152 + side_dir * 3.0,
                    86.0,
                ),
                (0.0, 0.0, 1.0),
                90 + dir * 90,
            ),
        )

        # Link: <half>_<side>_lower_arm_link
        lower_arm_link, _ = bom.get_assembly("robots/don1/link_lower_arm.py")
        side_assembly.add(
            lower_arm_link,
            name=half + "_" + side + "_lower_arm_link",
            loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
        )

        upper_arm_assembly = cq.Assembly()
        upper_arm_link, _ = bom.get_assembly("robots/don1/link_upper_arm.py")
        upper_arm_assembly.add(
            upper_arm_link,
            name=half + "_" + side + "_upper_arm_link",
            loc=cq.Location((0, 0, 0), (1, 0, 0), 0),
        )

        wheel_link, _ = bom.get_assembly("robots/don1/link_wheel.py")
        upper_arm_assembly.add(
            wheel_link,
            name=half + "_" + side + "_wheel_link",
            loc=cq.Location((0, -293.5, -75.2), (1, 0, 0), 90),
        )

        side_assembly.add(
            upper_arm_assembly,
            name=half + "_" + side + "_upper_arm_link",
            loc=cq.Location((0, -304.90, 108.75), (1, 0, 0), 39),
        )

        hip_assembly.add(
            side_assembly,
            name=half + "_" + side + "_lower_arm",
            loc=cq.Location((90, -3, 0), (0, 0, 1), 90 - 90 * side_dir),
        )

    half_assembly.add(
        hip_assembly,
        name=half + "_hip",
        loc=cq.Location((149.5, 0, -30), (0, 0, 1), 0),
    )

    result.add(
        half_assembly,
        loc=cq.Location((dir * 272.5, 0, -7), (0, 0, 1), 90 - 90 * dir),
        name=half + "_turn_table",
    )


if __name__ == "__main__":
    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    # This model is too large for VS Code to be able to render
    # try:
    #     ov.config.status()
    #     print("Visualizing...")
    #     ov.show(shape)
    # except:
    #     print('No VS Code or "OCP CAD Viewer" extension detected.')

    print("Generating STL...")
    shape.exportStl(models + "/generated_files/robots/don1/robot.stl", 0.5, 5.0)

    print("Generating SVG...")
    # len = shape.BoundingBox().DiagonalLength
    xlen = shape.BoundingBox().xlen
    ylen = shape.BoundingBox().ylen
    zlen = shape.BoundingBox().zlen
    len = max(xlen, ylen, zlen)
    if len > 300.0:
        len = 300.0
    exportSvgOpts["strokeWidth"] = len / 150.0
    cq.exporters.export(
        shape,
        models + "/generated_files/robots/don1/robot.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url=models + "/generated_files/robots/don1/robot.svg",
        write_to=models + "/generated_files/robots/don1/robot.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

    print("Generating BoM...")
    bom.write("Don1", models + "/generated_files/robots/don1/bom.md")
else:
    show_object(result, name="Don1")
