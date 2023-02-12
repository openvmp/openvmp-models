if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq

import sys

sys.path.append(".")
from lib.bom import Bom


result = cq.Assembly(name="turn_table_link")
bom = Bom()

# Get parts
channel, channel_name = bom.get_part("./parts/gobilda/structure-u-channel-2")
low_channel_1, low_channel_name_1 = bom.get_part(
    "./parts/gobilda/structure-u-channel-low-7"
)
low_channel_name_1 += "_1"
low_channel_2, low_channel_name_2 = bom.get_part(
    "./parts/gobilda/structure-u-channel-low-7"
)
low_channel_name_2 += "_2"


# Place parts
result.add(
    channel,
    name=channel_name,
    loc=cq.Location((98.5, 0, -8.50), (0, 0, 1), 90),
)
result.add(
    low_channel_1,
    name=low_channel_name_1,
    loc=cq.Location((98.5, 48, -8.50), (0, 0, 1), 90),
)
result.add(
    low_channel_2,
    name=low_channel_name_2,
    loc=cq.Location((-93.5, -48, -8.50), (0, 0, 1), -90),
)


if __name__ == "__main__":
    shape = result.toCompound()

    print("Generating STL...")
    shape.exportStl(
        "../platform/src/openvmp_robot_don1/meshes/turn_table.stl", 0.5, 5.0
    )
else:
    show_object(result, options={"bom": bom, "name": "turn_table_link"})
