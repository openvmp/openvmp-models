if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq

import cairosvg
import sys

sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts


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
        loc=cq.Location((4.0, -96.0, 0), (0, 1, 0), 90),
    )
    assembly_wormgear, assembly_wormgear_name = bom.get_assembly(
        "./robots/don1/assembly_wormgear.py"
    )
    half_assembly.add(
        assembly_wormgear,
        name=half + "_" + assembly_wormgear_name,
        loc=cq.Location((20.2, 31.3, 46.3), (0.58, -0.58, 0.58), 120.0),
    )
    worm_gear_shaft, worm_gear_shaft_name = bom.get_part(
        "./parts/gobilda/motion-shaft-8mmREX-72mm"
    )
    half_assembly.add(
        worm_gear_shaft,
        name=half + "_" + worm_gear_shaft_name,
        loc=cq.Location((26.0, 7.0, -68.5), (1.0, 0.0, 0.0), 90),
    )
    worm_gear_shaft_clip, worm_gear_shaft_clip_name = bom.get_part(
        "./parts/gobilda/motion-shaft-8mmREX-clip"
    )
    half_assembly.add(
        worm_gear_shaft_clip,
        name=half + "_" + worm_gear_shaft_clip_name,
        loc=cq.Location((26.0, 7.0, -68.5), (1.0, 0.0, 0.0), 90),
    )
    bearing, bearing_name = bom.get_part(
        "./parts/gobilda/motion-bearing-flanged-8mmREX"
    )
    bearing, bearing_name = bom.get_part(
        "./parts/gobilda/motion-bearing-flanged-8mmREX"
    )
    half_assembly.add(
        bearing,
        name=half + "_" + bearing_name + "_1",
        loc=cq.Location((-17.36, 0.02, -25.2), (1, 0, 0), 90.0),
    )
    half_assembly.add(
        bearing,
        name=half + "_" + bearing_name + "_2",
        loc=cq.Location((-17.36, 0.02, 20.0), (1, 0, 0), 90.0),
    )
    collar, collar_name = bom.get_part("./parts/gobilda/motion-collar-clamping-8mmREX")
    half_assembly.add(
        collar,
        name=half + "_" + collar_name,
        loc=cq.Location((1.2, 28.8, -20.7), (0.58, 0.58, -0.58), 240.0),
    )
    worm_shaft, worm_shaft_name = bom.get_part(
        "./parts/gobilda/motion-shaft-8mmREX-64mm"
    )
    half_assembly.add(
        worm_shaft,
        name=half + "_" + worm_shaft_name,
        loc=cq.Location((45.0, -67.5, 7.0), (0.71, -0.71, 0.0), 180),
    )
    qbm, qbm_name = bom.get_part("./parts/gobilda/structure-mount-quad-block")
    half_assembly.add(
        qbm,
        name=half + "_" + qbm_name,
        loc=cq.Location((-41.5, -24, 0.0), (0, 0, -1), 90),
    )
    worm_hub, worm_hub_name = bom.get_part("./parts/gobilda/motion-hub-sonic-8mmREX")
    half_assembly.add(
        worm_hub,
        name=half + "_" + worm_hub_name,
        loc=cq.Location((26.9, -41.7, -3.9), (0, 1, 0), 90),
    )
    worm_sprocket, worm_sprocket_name = bom.get_part(
        "./parts/gobilda/motion-sprocket-plastic-14mm-16t"
    )
    half_assembly.add(
        worm_sprocket,
        name=half + "_" + worm_sprocket_name,
        loc=cq.Location((21.0, -24, 0.0), (0, 1, 0), 90),
    )

    for side, side_dir in [("left", -1), ("right", 1)]:
        motor, motor_name = bom.get_part(
            "./parts/stepperonline/nema17-stepper-brake-72Ncm"
        )
        half_assembly.add(
            motor.rotate((0, 0, 0), (0, 0, 1), 90 - side_dir * 90),
            name=half + "_" + side + "_" + motor_name,
            loc=cq.Location((0, -side_dir * 72, 0), (0.71, 0, 0.71), 180),
        )
        pad, pad_name = bom.get_part("./parts/custom/nema17-flush-pad")
        pad, pad_name = bom.get_part("./parts/custom/nema17-flush-pad")
        half_assembly.add(
            pad,
            name=half + "_" + side + "_" + pad_name + "_1",
            loc=cq.Location((0.0, -side_dir * 72, 0), (0.71, 0, 0.71), 180),
        )
        half_assembly.add(
            pad,
            name=half + "_" + side + "_" + pad_name + "_2",
            loc=cq.Location((2.0, -side_dir * 72, 0), (0.71, 0, 0.71), 180),
        )
        motor_bearing, motor_bearing_name = bom.get_part(
            "./parts/gobilda/motion-bearing-flanged-5mm"
        )
        half_assembly.add(
            motor_bearing,
            name=half + "_" + side + "_" + motor_bearing_name,
            loc=cq.Location((2.50, -side_dir * 72, 0), (0, 0, -1), 90),
        )
        motor_spacer, motor_spacer_name = bom.get_part(
            "./parts/gobilda/hardware-spacer-plastic-5mm-1mm"
        )
        half_assembly.add(
            motor_spacer,
            name=half + "_" + side + "_" + motor_spacer_name,
            loc=cq.Location((-8.5, -side_dir * 72, 0.0), (0, 0, 1), 90),
        )
        motor_hub, motor_hub_name = bom.get_part("./parts/gobilda/motion-hub-sonic-5mm")
        half_assembly.add(
            motor_hub,
            name=half + "_" + side + "_" + motor_hub_name,
            loc=cq.Location((8.5, -side_dir * 72 - 4.6, -14.5), (0, 1, 0), 90),
        )
        motor_sprocket, motor_sprocket_name = bom.get_part(
            "./parts/gobilda/motion-sprocket-steel-14mm-14t"
        )
        half_assembly.add(
            motor_sprocket,
            name=half + "_" + side + "_" + motor_sprocket_name,
            loc=cq.Location((22.0, -side_dir * 72, 0.0), (0, 1, 0), 90),
        )

    result.add(
        half_assembly,
        name=half + "_motion",
        loc=cq.Location((dir * 290.0, 0, 27.0), (0, 0, 1), -(dir - 1) * 90),
    )

if __name__ == "__main__":
    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating STL...")
    shape.exportStl("../platform/src/openvmp_robot_don1/meshes/base.stl", 0.5, 5.0)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        "generated_files/robots/don1/base.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url="generated_files/robots/don1/base.svg",
        write_to="generated_files/robots/don1/base.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "base_link",
        },
    )
