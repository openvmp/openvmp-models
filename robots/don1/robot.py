if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery.cqgi as cqgi
import cadquery as cq

import sys

sys.path.append(".")
from lib.bom import Bom

result = cq.Assembly()
bom = Bom()

# Link: base_link
bom.add_assembly(result, "./robots/don1/link_base.py")

# Link: front_turn_table_link
front_turn_table_link, _ = bom.get_assembly("./robots/don1/link_turn_table.py")
result.add(
    front_turn_table_link,
    name="front_turn_table_link",
    loc=cq.Location((272.5, 0, -7), (0, 0, 1), 0),
)

# Link: rear_turn_table_link
rear_turn_table_link = bom.get_assembly("./robots/don1/link_turn_table.py")
result.add(
    front_turn_table_link,
    name="rear_turn_table_link",
    loc=cq.Location((-272.5, 0, -7), (0, 0, 1), 180),
)

if __name__ == "__main__":
    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating STL...")
    cq.exporters.export(
        shape,
        "generated_files/robots/don1/robot.stl",
        opt={"linearDeflection": 0.01, "angularDeflection": 0.5},
    )

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        "generated_files/robots/don1/robot.svg",
        opt={
            "width": 500,
            "height": 200,
            "marginLeft": 12,
            "marginTop": 12,
            "showAxes": False,
            "projectionDir": [0.5, 0.25, 0.5],
            "strokeWidth": 0.25,
            "strokeColor": [64, 255, 64],
            "hiddenColor": [32, 64, 32],
            "showHidden": True,
        },
    )

    print("Generating BoM...")
    bom.write("generated_files/robots/don1/bom.md")
else:
    show_object(result, name="Don1")
