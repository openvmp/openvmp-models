if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import cadquery as cq

import cairosvg
import sys

sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts


result = cq.Assembly(name="lower_arm_link")
bom = Bom()

# - thigh structure
channel, channel_name = bom.get_part("./parts/gobilda/structure-u-channel-5")
channel, channel_name = bom.get_part("./parts/gobilda/structure-u-channel-5")
result.add(
    channel,
    name=channel_name + "_1",
    loc=cq.Location((0, -178, -21.50), (0, 1, 0), 180),
)
result.add(
    channel,
    name=channel_name + "_2",
    loc=cq.Location((0, -204.66, 39.23), (0, 0.38, 0.92), 180),
)
bracket, bracket_name = bom.get_part("./parts/gobilda/structure-bracket-flat-2-3")
bracket, bracket_name = bom.get_part("./parts/gobilda/structure-bracket-flat-2-3")
result.add(
    bracket,
    name=bracket_name + "_1",
    loc=cq.Location((24.0, -187.65, 20.0), (0.70, 0.70, -0.14), 164.14),
)
result.add(
    bracket,
    name=bracket_name + "_2",
    loc=cq.Location((-26.5, -187.65, 20.0), (0.70, 0.70, -0.14), 164.14),
)

# - radial load support
qbm, qbm_name = bom.get_part("./parts/gobilda/structure-mount-quad-block")
qbm, qbm_name = bom.get_part("./parts/gobilda/structure-mount-quad-block")
result.add(
    qbm,
    name=qbm_name + "_1",
    loc=cq.Location((0.0, -34.0, 0.0), (0, 0, 1), 180),
)
result.add(
    qbm,
    name=qbm_name + "_2",
    loc=cq.Location((0.0, -50.0, 0.0), (0, 0, 1), 180),
)
shaft, shaft_name = bom.get_part("./parts/gobilda/motion-shaft-8mmREX-56mm")
result.add(
    shaft,
    name=shaft_name,
    loc=cq.Location((-43.4, 17, -7.0), (0, 0, 1), 180),
)
# shaft_clip, shaft_clip_name = bom.get_part("./parts/gobilda/motion-shaft-8mmREX-clip")
# result.add(
#     shaft_clip,
#     name=shaft_clip_name,
#     loc=cq.Location((6.5, -36.4, 44.0), (0.0, 1.0, 0.0), 270),
# )
bearing, bearing_name = bom.get_part("./parts/gobilda/motion-bearing-flanged-8mmREX")
bearing, bearing_name = bom.get_part("./parts/gobilda/motion-bearing-flanged-8mmREX")
result.add(
    bearing,
    name=bearing_name + "_1",
    loc=cq.Location((0.0, -55.0, 0.0), (0, 0, 1), 0.0),
)
result.add(
    bearing,
    name=bearing_name + "_2",
    loc=cq.Location((0.0, -34.0, 0.0), (0, 0, 1), 180.0),
)
spacer_plastic, spacer_plastic_name = bom.get_part(
    "./parts/gobilda/hardware-spacer-plastic-8mm-1mm"
)
spacer_plastic, spacer_plastic_name = bom.get_part(
    "./parts/gobilda/hardware-spacer-plastic-8mm-1mm"
)
spacer_plastic, spacer_plastic_name = bom.get_part(
    "./parts/gobilda/hardware-spacer-plastic-8mm-1mm"
)
spacer_plastic, spacer_plastic_name = bom.get_part(
    "./parts/gobilda/hardware-spacer-plastic-8mm-1mm"
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_1",
    loc=cq.Location((0.0, -41.0, 0.0), (0, 0, 1), 0.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_2",
    loc=cq.Location((0.0, -40.0, 0.0), (0, 0, 1), 0.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_3",
    loc=cq.Location((0.0, -34.0, 0.0), (0, 0, 1), 0.0),
)
result.add(
    spacer_plastic,
    name=spacer_plastic_name + "_4",
    loc=cq.Location((0.0, -33.0, 0.0), (0, 0, 1), 0.0),
)
collar, collar_name = bom.get_part("./parts/gobilda/motion-collar-clamping-8mmREX")
result.add(
    collar,
    name=collar_name,
    loc=cq.Location((-28.9, -50.6, -18.8), (0, 0, 1), 180.0),
)

# - thigh locomotion
motor, motor_name = bom.get_part("./parts/stepperonline/nema17-stepper-brake-72Ncm")
result.add(
    motor,
    name=motor_name + "_1",
    loc=cq.Location((0.0, -141.5, 0.0), (-1, 0, 0), 90),
)
mount, mount_name = bom.get_part("./parts/custom/nema17-mount")
result.add(
    mount,
    name=mount_name,
    loc=cq.Location((0.0, -153.0, 21.5), (0, 0, 1), 0.0),
)
gearbox, gearbox_name = bom.get_part(
    "./parts/stepperonline/nema17-gearbox-planetary-10"
)
result.add(
    gearbox,
    name=gearbox_name,
    loc=cq.Location((-9.5, -145.2, 0.0), (-1, 0, 0), 90.0),
)
coupler, coupler_name = bom.get_part("./parts/gobilda/motion-coupler-hyper-8mm-8mmREX")
result.add(
    coupler,
    name=coupler_name,
    loc=cq.Location((22.15, -58.4, -17.5), (0, 0, 1), 0.0),
)


# - knee
worm_gear_shaft, worm_gear_shaft_name = bom.get_part(
    "./parts/gobilda/motion-shaft-8mmREX-80mm"
)
result.add(
    worm_gear_shaft,
    name=worm_gear_shaft_name,
    loc=cq.Location((63.35, -261.41, 115.1), (0.15, -0.15, 0.98), 91.4),
)
bearing, bearing_name = bom.get_part("./parts/gobilda/motion-bearing-flanged-8mmREX")
bearing, bearing_name = bom.get_part("./parts/gobilda/motion-bearing-flanged-8mmREX")
result.add(
    bearing,
    name="worm_gear_" + bearing_name + "_1",
    loc=cq.Location((20.0, -304.9, 108.8), (0, 0, -1), 90.0),
)
result.add(
    bearing,
    name="worm_gear_" + bearing_name + "_2",
    loc=cq.Location((-20.0, -304.9, 108.8), (0, 0, 1), 90.0),
)
spacer_steel, spacer_steel_name = bom.get_part(
    "./parts/gobilda/hardware-spacer-steel-8mm-4mm"
)
spacer_steel, spacer_steel_name = bom.get_part(
    "./parts/gobilda/hardware-spacer-steel-8mm-4mm"
)
result.add(
    spacer_steel,
    name=spacer_steel_name + "_1",
    loc=cq.Location((27.0, -304.9, 108.8), (0, 0, -1), 90),
)
result.add(
    spacer_steel,
    name=spacer_steel_name + "_2",
    loc=cq.Location((-27.0, -304.9, 108.8), (0, 0, -1), 90),
)

# - knee worm
assembly_wormgear, assembly_wormgear_name = bom.get_assembly(
    "./robots/don1/assembly_wormgear.py"
)
result.add(
    assembly_wormgear,
    name=assembly_wormgear_name,
    loc=cq.Location((46.2, -300.46, 157.63), (1.0, 0.0, 0.0), 225.0),
)
worm_shaft, worm_shaft_name = bom.get_part("./parts/gobilda/motion-shaft-8mmREX-64mm")
result.add(
    worm_shaft,
    name="worm_" + worm_shaft_name,
    loc=cq.Location((43.35, -249.26, 140.33), (1, 0, 0), 225),
)
qbm, qbm_name = bom.get_part("./parts/gobilda/structure-mount-quad-block")
result.add(
    qbm,
    name="worm_" + qbm_name,
    loc=cq.Location((0.0, -304.76, 74.95), (1, 0, 0), 45),
)
worm_hub, worm_hub_name = bom.get_part("./parts/gobilda/motion-hub-sonic-8mmREX")
result.add(
    worm_hub,
    name="worm_" + worm_hub_name,
    loc=cq.Location((3.9, -271.66, 133.08), (-1, 0, 0), 45),
)
worm_sprocket, worm_sprocket_name = bom.get_part(
    "./parts/gobilda/motion-sprocket-plastic-14mm-16t"
)
result.add(
    worm_sprocket,
    name="worm_" + worm_sprocket_name,
    loc=cq.Location((0.0, -263.41, 116.32), (-1, 0, 0), 45),
)

# - knee motor
motor, motor_name = bom.get_part("./parts/stepperonline/nema17-stepper-brake-72Ncm")
result.add(
    motor,
    name=motor_name + "_2",
    loc=cq.Location((0.0, -241.25, 70.53), (0, 0.38, 0.92), 180),
)
pad, pad_name = bom.get_part("./parts/custom/nema17-flush-pad")
pad, pad_name = bom.get_part("./parts/custom/nema17-flush-pad")
result.add(
    pad,
    name=pad_name + "_1",
    loc=cq.Location((0.0, -241.25, 70.53), (0.0, 0.38, 0.92), 180),
)
result.add(
    pad,
    name=pad_name + "_2",
    loc=cq.Location((0.0, -239.84, 71.95), (0.0, 0.38, 0.92), 180),
)
motor_bearing, motor_bearing_name = bom.get_part(
    "./parts/gobilda/motion-bearing-flanged-5mm"
)
result.add(
    motor_bearing,
    name=motor_bearing_name,
    loc=cq.Location((0.0, -239.84, 71.95), (0, 0.92, 0.38), 180),
)
motor_spacer, motor_spacer_name = bom.get_part(
    "./parts/gobilda/hardware-spacer-plastic-5mm-1mm"
)
result.add(
    motor_spacer,
    name=motor_spacer_name,
    loc=cq.Location((0.0, -236.30, 75.49), (1, 0, 0), 45),
)
motor_hub, motor_hub_name = bom.get_part("./parts/gobilda/motion-hub-sonic-5mm")
result.add(
    motor_hub,
    name=motor_hub_name,
    loc=cq.Location((14.60, -238.88, 79.41), (-1, 0, 0), 45),
)
motor_sprocket, motor_sprocket_name = bom.get_part(
    "./parts/gobilda/motion-sprocket-plastic-14mm-16t"
)
result.add(
    motor_sprocket,
    name=motor_sprocket_name,
    loc=cq.Location((0.0, -229.64, 82.13), (-1, 0, 0), 45),
)


if __name__ == "__main__":
    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating STL...")
    shape.exportStl("../platform/src/openvmp_robot_don1/meshes/lower_arm.stl", 0.5, 5.0)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        "generated_files/robots/don1/lower_arm.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url="generated_files/robots/don1/lower_arm.svg",
        write_to="generated_files/robots/don1/lower_arm.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "lower_arm_link",
        },
    )
