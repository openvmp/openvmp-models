if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery.cqgi as cqgi
import cadquery as cq

import sys

sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts

result = cq.Assembly()
bom = Bom()

# Link: base_link
bom.add_assembly(result, "./robots/don1/link_base.py")

for half, dir in [("front", 1), ("rear", -1)]:
    half_assembly = cq.Assembly()
    # Link: <half>_turn_table_link
    turn_table_link, _ = bom.get_assembly("./robots/don1/link_turn_table.py")
    half_assembly.add(
        turn_table_link,
        name=half + "_turn_table_link",
        loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
    )

    body_assembly = cq.Assembly()
    # Link: <half>_turn_table_link
    body_link, _ = bom.get_assembly("./robots/don1/link_body.py")
    body_assembly.add(
        body_link,
        name=half + "_body_link",
        loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
    )

    for side, side_dir in [("left", 1), ("right", -1)]:
        side_assembly = cq.Assembly()
        # Link: <half>_<side>_lower_arm_link
        lower_arm_link, _ = bom.get_assembly("./robots/don1/link_lower_arm.py")
        side_assembly.add(
            lower_arm_link,
            name=half + "_" + side + "_lower_arm_link",
            loc=cq.Location((0, 0, 0), (0, 0, 1), 0),
        )

        upper_arm_link, _ = bom.get_assembly("./robots/don1/link_upper_arm.py")
        side_assembly.add(
            upper_arm_link,
            name=half + "_" + side + "_upper_arm_link",
            loc=cq.Location((0, -300.50, 112), (1, 0, 0), 39),
        )

        body_assembly.add(
            side_assembly,
            name=half + "_" + side + "_lower_arm",
            loc=cq.Location((90, -3, 0), (0, 0, 1), 90 - 90 * side_dir),
        )

    half_assembly.add(
        body_assembly,
        name=half + "_body",
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

    print("Generating STL...")
    shape.exportStl("generated_files/robots/don1/robot.stl", 0.5, 5.0)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        "generated_files/robots/don1/robot.svg",
        opt=exportSvgOpts,
    )

    print("Generating BoM...")
    bom.write("generated_files/robots/don1/bom.md")
else:
    show_object(result, name="Don1")
