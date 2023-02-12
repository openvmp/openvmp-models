if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq

import sys

sys.path.append(".")
from lib.bom import Bom


result = cq.Assembly(name="body_link")
bom = Bom()

# Get parts
channel_1, channel_name_1 = bom.get_part("./parts/gobilda/structure-u-channel-9")
channel_2, channel_name_2 = bom.get_part("./parts/gobilda/structure-u-channel-9")
channel_3, channel_name_3 = bom.get_part("./parts/gobilda/structure-u-channel-9")
channel_4, channel_name_4 = bom.get_part("./parts/gobilda/structure-u-channel-9")
side_channel_1, side_channel_name_1 = bom.get_part(
    "./parts/gobilda/structure-u-channel-2"
)
side_channel_2, side_channel_name_2 = bom.get_part(
    "./parts/gobilda/structure-u-channel-2"
)

channel_name_1 += "_1"
channel_name_2 += "_2"
channel_name_3 += "_3"
channel_name_4 += "_4"
side_channel_name_1 += "_1"
side_channel_name_2 += "_2"

# Place parts
# - main channels
result.add(
    channel_1,
    name=channel_name_1,
    loc=cq.Location((210.5, 0, 21.35), (0, 0, 1), 90),
)
result.add(
    channel_2,
    name=channel_name_2,
    loc=cq.Location((210.5, 0, 26.35), (0.71, -0.71, 0), 180),
)
result.add(
    channel_3,
    name=channel_name_3,
    loc=cq.Location((210.5, -48, 69.35), (0, 0, 1), 90),
)
result.add(
    channel_4,
    name=channel_name_4,
    loc=cq.Location((210.5, 48, 69.35), (0, 0, 1), 90),
)

# - side channels
result.add(
    side_channel_1,
    name=side_channel_name_1,
    loc=cq.Location((26.5, -96, 69.35), (0, 0, 1), 90),
)
result.add(
    side_channel_2,
    name=side_channel_name_2,
    loc=cq.Location((26.5, 96, 69.35), (0, 0, 1), 90),
)


if __name__ == "__main__":
    shape = result.toCompound()

    print("Generating STL...")
    shape.exportStl("../platform/src/openvmp_robot_don1/meshes/body.stl", 0.5, 5.0)
else:
    show_object(result, options={"bom": bom, "name": "body_link"})
