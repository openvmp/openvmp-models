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


if __name__ == "__main__":
    shape = result.toCompound()

    print("Generating STL...")
    cq.exporters.export(
        shape,
        "../platform/src/openvmp_robot_don1/meshes/base.stl",
        opt={"linearDeflection": 0.01, "angularDeflection": 0.5},
    )
else:
    show_object(result, options={"bom": bom, "name": "base_link"})
