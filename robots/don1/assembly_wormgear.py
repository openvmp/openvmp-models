if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import ocp_vscode as ov
import cadquery as cq

import sys

sys.path.append("models")
sys.path.append("..")
sys.path.append(".")
from lib.bom import Bom
from lib.common import get_models_dir


models = get_models_dir()
bom = Bom()
result = cq.Assembly(name="worm_gear_assembly")

# - worm axle
worm, worm_name = bom.get_part("parts/gobilda/motion-worm-8mmREX")
result.add(
    worm,
    name=worm_name,
    loc=cq.Location(
        # (-41.0 - 5.26, 39.5 + 0.48, 21.50 + 9.93),
        (-41.0, 39.5, 21.50),  # TODO(clairbee): why????
        (0, 0, 1),
        0,
    ),
)
bearing, bearing_name = bom.get_part("parts/gobilda/motion-bearing-flanged-8mmREX", 2)
result.add(
    bearing,
    name=bearing_name + "_1",
    loc=cq.Location((-46.2, 12.4, 55.4), (0, 0, 1), 0.0),
)
result.add(
    bearing,
    name=bearing_name + "_2",
    loc=cq.Location((-46.2, 62.5, 55.4), (0, 0, 1), 180.0),
)
spacer_plastic, spacer_plastic_name = bom.get_part(
    "parts/gobilda/hardware-spacer-plastic-8mm-1mm", 3
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_1",
    loc=cq.Location((-46.2, 54.5, 55.4), (0, 0, 1), 0.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_2",
    loc=cq.Location((-46.2, 54.5 + 1.0, 55.4), (0, 0, 1), 0.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_3",
    loc=cq.Location((-46.2, 54.5 + 2.0, 55.4), (0, 0, 1), 0.0),
)
spacer_steel, spacer_steel_name = bom.get_part(
    "parts/gobilda/hardware-spacer-steel-8mm-4mm"
)
result.add(
    spacer_steel,
    name=spacer_steel_name,
    loc=cq.Location((-46.2, 19.5, 55.4), (0, 0, 1), 0.0),
)

# - worm gear axle
worm_gear, worm_gear_name = bom.get_part("parts/gobilda/motion-worm-gear-28t")
result.add(
    worm_gear,
    name=worm_gear_name,
    loc=cq.Location((-47.14 + 0.8, 2.0 + 35.74, 31.35), (1, 0, 0), 43.6),
)
worm_gear_hub, worm_gear_hub_name = bom.get_part(
    "parts/gobilda/motion-hub-sonic-8mmREX"
)
result.add(
    worm_gear_hub,
    name=worm_gear_hub_name,
    loc=cq.Location((-40.5 + 0.9, 20.0, 27.5), (0, 1, 0), 90),
)


if __name__ == "__main__":
    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    try:
        ov.config.status()
        print("Visualizing...")
        ov.show(shape)
    except:
        print('No VS Code or "OCP CAD Viewer" extension detected.')

    print("No need to generate any STL.")
else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "worm_gear_assembly",
        },
    )
