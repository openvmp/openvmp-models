if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq
import sys

sys.path.append(".")
from lib.bom import Bom


result = cq.Assembly(name="base_link")
bom = Bom()

bom.add_part(result, "./parts/custom/don1_board_top")
bom.add_part(result, "./parts/custom/don1_board_bottom")

for half, dir in [("front", 1), ("rear", -1)]:
    half_assembly = cq.Assembly()

    channel, channel_name = bom.get_part("./parts/gobilda/structure-u-channel-7")
    half_assembly.add(
        channel,
        name=half + "_" + channel_name,
        loc=cq.Location((0, -96, 0), (0, 1, 0), 0),
    )

    motor, motor_name = bom.get_part("./parts/stepperonline/nema17-stepper-brake-72Ncm")
    for side, side_dir in [("left", -1), ("right", 1)]:
        half_assembly.add(
            motor.rotate((0, 0, 0), (0, 0, 1), 90 - side_dir * 90),
            name=half + "_" + side + "_" + motor_name,
            loc=cq.Location((-2 * dir, side_dir * 72, 0), (0, 1, 0), 0),
        )

    result.add(
        half_assembly,
        name=half + "_motion",
        loc=cq.Location((dir * 294, 0, 27), (0, 1, 0), dir * 90),
    )

if __name__ == "__main__":
    shape = result.toCompound()

    print("Generating STL...")
    shape.exportStl("../platform/src/openvmp_robot_don1/meshes/base.stl", 0.5, 5.0)
else:
    show_object(result, options={"bom": bom, "name": "base_link"})
