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
result = cq.Assembly(name="turn_table_link")

# - structure
turntable, turntable_name = bom.get_part("parts/custom/don1_turntable")
result.add(
    turntable,
    name=turntable_name,
    loc=cq.Location((0, 0, 2.5), (0, 0, 1), 0),
)
tt_attach_hex, tt_attach_hex_name = bom.get_part(
    "parts/custom/turntable_attachment_hex"
)
result.add(
    tt_attach_hex,
    name=tt_attach_hex_name,
    loc=cq.Location((250.0, 0, 139.5), (0, 1, 0), 180),
)
channel, channel_name = bom.get_part("parts/gobilda/structure-u-channel-2")
result.add(
    channel,
    name=channel_name,
    loc=cq.Location((98.5, 0, -8.50), (0, 0, 1), 90),
)
low_channel, low_channel_name = bom.get_part(
    "parts/gobilda/structure-u-channel-low-7", 2
)
result.add(
    low_channel,
    name=low_channel_name + "_1",
    loc=cq.Location((98.5, 48, -8.50), (0, 0, 1), 90),
)
result.add(
    low_channel,
    name=low_channel_name + "_2",
    loc=cq.Location((-93.5, -48, -8.50), (0, 0, 1), -90),
)

# - radial load support
qbm, qbm_name = bom.get_part("parts/gobilda/structure-mount-quad-block", 2)
result.add(
    qbm,
    name=qbm_name + "_1",
    loc=cq.Location((82.5, 0.0, -30.0), (0, 0, 1), 90),
)
result.add(
    qbm,
    name=qbm_name + "_2",
    loc=cq.Location((98.5, 0.0, -30.0), (0, 0, 1), 90),
)
shaft, shaft_name = bom.get_part("parts/gobilda/motion-shaft-8mmREX-64mm")
result.add(
    shaft,
    name=shaft_name,
    loc=cq.Location((152.0, 43.40, -37.0), (0, 0, 1), 90),
)
shaft_clip, shaft_clip_name = bom.get_part("parts/gobilda/motion-shaft-8mmREX-clip")
result.add(
    shaft_clip,
    name=shaft_clip_name,
    loc=cq.Location((98.0, -7.0, 14.0), (0.58, 0.58, 0.58), 240),
)
bearing, bearing_name = bom.get_part("parts/gobilda/motion-bearing-flanged-8mmREX", 2)
result.add(
    bearing,
    name=bearing_name + "_1",
    loc=cq.Location((98.5, 0.0, -30.0), (0, 0, 1), 90.0),
)
result.add(
    bearing,
    name=bearing_name + "_2",
    loc=cq.Location((77.5, 0.0, -30.0), (0, 0, -1), 90.0),
)
spacer_plastic, spacer_plastic_name = bom.get_part(
    "parts/gobilda/hardware-spacer-plastic-8mm-1mm", 4
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_1",
    loc=cq.Location((92.5, 0.0, -30.0), (0, 0, 1), 90.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_2",
    loc=cq.Location((93.5, 0.0, -30.0), (0, 0, 1), 90.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_3",
    loc=cq.Location((99.5, 0.0, -30.0), (0, 0, 1), 90.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_4",
    loc=cq.Location((100.5, 0.0, -30.0), (0, 0, 1), 90.0),
)
collar, collar_name = bom.get_part("parts/gobilda/motion-collar-clamping-8mmREX")
result.add(
    collar,
    name=collar_name,
    loc=cq.Location((82.0, 28.87, -48.87), (0, 0, 1), 90.0),
)

# - locomotion
motor, motor_name = bom.get_part("parts/stepperonline/nema17-stepper-brake-72Ncm")
result.add(
    motor,
    name=motor_name,
    loc=cq.Location((-18.25, 0.0, -30.0), (0.58, 0.58, 0.58), 120.0),
)
mount, mount_name = bom.get_part("parts/custom/nema17-mount-wide")
result.add(
    mount,
    name=mount_name,
    loc=cq.Location((-29.0, 2.5, -8.5), (0, 0, -1), 90.0),
)
gearbox, gearbox_name = bom.get_part("parts/stepperonline/nema17-gearbox-planetary-100")
result.add(
    gearbox,
    name=gearbox_name,
    loc=cq.Location((-10.55, -0.8, -20.5), (0, 1, 0), 90.0),
)
coupler, coupler_name = bom.get_part("parts/gobilda/motion-coupler-hyper-8mm-8mmREX")
result.add(
    coupler,
    name=coupler_name,
    loc=cq.Location((74.8, -22.15, -47.4), (0, 0, -1), 90.0),
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

    print("Generating STL...")
    shape.exportStl(
        models + "/../platform/src/openvmp_robot_don1/meshes/turn_table.stl", 0.5, 5.0
    )

    print("Generating SVG...")
    exportSvgOpts["projectionDir"] = [0.5, -0.25, 0.5]
    cq.exporters.export(
        shape,
        models + "/generated_files/robots/don1/turn_table.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url=models + "/generated_files/robots/don1/turn_table.svg",
        write_to=models + "/generated_files/robots/don1/turn_table.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "turn_table_link",
        },
    )
