if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq

import sys

sys.path.append(".")
from lib.bom import Bom


result = cq.Assembly(name="upper_arm_link")
bom = Bom()

# Get parts
channel_1, channel_name_1 = bom.get_part("./parts/gobilda/structure-u-channel-7")
channel_2, channel_name_2 = bom.get_part("./parts/gobilda/structure-u-channel-7")

channel_name_1 += "_1"
channel_name_2 += "_2"

# Place parts
# - main channels
result.add(
    channel_1,
    name=channel_name_1,
    loc=cq.Location((0, -268, -89.50), (0, 1, 0), 180),
)
result.add(
    channel_2,
    name=channel_name_2,
    loc=cq.Location((0, -223.00, -284.00), (0, 0.71, 0.71), 180),
)


if __name__ == "__main__":
    shape = result.toCompound()

    print("Generating STL...")
    shape.exportStl("../platform/src/openvmp_robot_don1/meshes/upper_arm.stl", 0.5, 5.0)
else:
    show_object(result, options={"bom": bom, "name": "upper_arm_link"})
