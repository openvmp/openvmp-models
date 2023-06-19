if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq

import sys

sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts


result = cq.Assembly(name="upper_arm_link")
bom = Bom()

# - main channels
channel, channel_name = bom.get_part("./parts/gobilda/structure-u-channel-7")
result.add(
    channel,
    name=channel_name + "_1",
    loc=cq.Location((0, -276.8, -53.7), (0, 0, 1), 0),
)
channel, channel_name = bom.get_part("./parts/gobilda/structure-u-channel-7")
result.add(
    channel,
    name=channel_name + "_2",
    loc=cq.Location((0, -231.3, -291.2), (0, 0.71, 0.71), 180),
)

# - radial load support
qbm, qbm_name = bom.get_part("./parts/gobilda/structure-mount-quad-block")
qbm, qbm_name = bom.get_part("./parts/gobilda/structure-mount-quad-block")
result.add(
    qbm,
    name=qbm_name + "_1",
    loc=cq.Location((0.0, -276.8, -75.2), (0, 0, 1), 0),
)
result.add(
    qbm,
    name=qbm_name + "_2",
    loc=cq.Location((0.0, -236.8, -75.2), (0, 0, 1), 0),
)
bearing, bearing_name = bom.get_part("./parts/gobilda/motion-bearing-flanged-6mm")
bearing, bearing_name = bom.get_part("./parts/gobilda/motion-bearing-flanged-6mm")
result.add(
    bearing,
    name=bearing_name + "_1",
    loc=cq.Location((0.0, -276.8, -75.2), (0, 0, 1), 0),
)
result.add(
    bearing,
    name=bearing_name + "_2",
    loc=cq.Location((0.0, -231.8, -75.2), (0, 0, 1), 180),
)
shaft, shaft_name = bom.get_part("./parts/gobilda/motion-shaft-6mmD-70mm")
result.add(
    shaft,
    name=shaft_name,
    loc=cq.Location((0.0, -293.5, -75.2), (0, 0, 1), 0),
)
wheel, wheel_name = bom.get_part("./parts/dfrobot/rubber-wheel")
result.add(
    wheel,
    name=wheel_name,
    loc=cq.Location((-90.5, -293.5 - 12.0, -75.2 - 48.0), (0, 0, 1), 0),
)
hook, hook_name = bom.get_part("./parts/custom/hook")
result.add(
    hook,
    name=hook_name,
    loc=cq.Location((0.0, -252.8, -291.2), (0, 0, 1), 0),
)

# - symmetric parts
symm = cq.Assembly(name="foot_symmetrical")
sonic_hub, sonic_hub_name = bom.get_part("./parts/gobilda/motion-hub-sonic-8mmREX")
sonic_hub, sonic_hub_name = bom.get_part("./parts/gobilda/motion-hub-sonic-8mmREX")
symm.add(
    sonic_hub,
    name=sonic_hub_name,
    loc=cq.Location((25.75, -17.7, 3.9), (0.0, -1.0, 0.0), 90),
)
bracket, bracket_name = bom.get_part("./parts/gobilda/structure-bracket-flat-1-2")
bracket, bracket_name = bom.get_part("./parts/gobilda/structure-bracket-flat-1-2")
symm.add(
    bracket,
    name=bracket_name,
    loc=cq.Location((30.76, 0.0, 0.0), (0.68, 0.68, -0.28), 148.60),
)
bracket, bracket_name = bom.get_part("./parts/gobilda/structure-bracket-flat-2-3")
bracket, bracket_name = bom.get_part("./parts/gobilda/structure-bracket-flat-2-3")
symm.add(
    bracket,
    name=bracket_name,
    loc=cq.Location((27.0, -83.13, -55.14), (0.70, 0.70, 0.14), 195.85),
)
nut, nut_name = bom.get_part("./parts/gobilda/hardware-nut-m4-0.7mm")
nut, nut_name = bom.get_part("./parts/gobilda/hardware-nut-m4-0.7mm")
nut, nut_name = bom.get_part("./parts/gobilda/hardware-nut-m4-0.7mm")
nut, nut_name = bom.get_part("./parts/gobilda/hardware-nut-m4-0.7mm")
nut, nut_name = bom.get_part("./parts/gobilda/hardware-nut-m4-0.7mm")
nut, nut_name = bom.get_part("./parts/gobilda/hardware-nut-m4-0.7mm")
symm.add(
    nut,
    name=nut_name + "_1",
    loc=cq.Location((25.5, -124.7, -59.2), (0.0, 1.0, 0.0), 90.0),
)
symm.add(
    nut,
    name=nut_name + "_2",
    loc=cq.Location((25.5, -124.7, -67.2), (0.0, 1.0, 0.0), 90.0),
)
symm.add(
    nut,
    name=nut_name + "_3",
    loc=cq.Location((25.5, -100.7, -59.2), (0.0, 1.0, 0.0), 90.0),
)
conn, conn_name = bom.get_part("./parts/gobilda/hardware-plate-channel-conn")
conn, conn_name = bom.get_part("./parts/gobilda/hardware-plate-channel-conn")
symm.add(
    conn,
    name=conn_name,
    loc=cq.Location((24.10, -252.8, -99.2), (0.0, 0.0, -1.0), 90.0),
)

result.add(symm)
symm_shape = symm.toCompound()
result.add(symm_shape.mirror(mirrorPlane="YZ"))


if __name__ == "__main__":
    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating STL...")
    shape.exportStl("../platform/src/openvmp_robot_don1/meshes/upper_arm.stl", 0.5, 5.0)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        "generated_files/robots/don1/upper_arm.svg",
        opt=exportSvgOpts,
    )
else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "upper_arm_link",
        },
    )
