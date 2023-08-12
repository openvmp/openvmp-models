if __name__ != "__cqgi__":
    from cq_server.ui import ui, show_object
import ocp_vscode as ov
import cadquery as cq

import cairosvg
import sys

sys.path.append("models")
sys.path.append("..")
sys.path.append(".")
sys.path.append("models")
from lib.bom import Bom
from lib.doc import exportSvgOpts
from lib.export import exportOBJ
from lib.common import get_models_dir


models = get_models_dir()
bom = Bom()
result = cq.Assembly(name="body_link")

# Load parts
channel, channel_name = bom.get_part("parts/gobilda/structure-u-channel-9", 4)
qbm, qbm_name = bom.get_part("parts/gobilda/structure-mount-quad-block", 8)
standoff, standoff_name = bom.get_part("parts/gobilda/structure-standoff-m4-43mm", 8)
wheel, wheel_name = bom.get_part("parts/dfrobot/rubber-wheel")
hyper_hub, hyper_hub_name = bom.get_part("parts/gobilda/motion-hub-hyper-8mmREX", 3)
shaft6, shaft6_name = bom.get_part("parts/gobilda/motion-shaft-6mmD-70mm")
side_channel, side_channel_name = bom.get_part("parts/gobilda/structure-u-channel-2", 2)
servo_mount, servo_mount_name = bom.get_part(
    "parts/gobilda/structure-mount-servo-43mm-std", 6
)
servo_hs488hb, servo_hs488hb_name = bom.get_part(
    "parts/gobilda/motion-servo-hs-488hb", 6
)
bearing6, bearing6_name = bom.get_part("parts/gobilda/motion-bearing-flanged-6mm", 2)
collar6, collar6_name = bom.get_part("parts/gobilda/motion-collar-set-6mm", 2)
beam, beam_name = bom.get_part("parts/gobilda/structure-beam-15", 2)
servo_attachment, servo_attachment_name = bom.get_part(
    "parts/gobilda/motion-servo-attach-hub-low-25t", 2
)
servo_arm_attachment, servo_arm_attachment_name = bom.get_part(
    "parts/gobilda/motion-servo-attach-arm-25t", 2
)
camera_channel, camera_channel_name = bom.get_part(
    "parts/gobilda/structure-u-channel-low-3", 2
)

# - main structure
#   - channels
result.add(
    channel,
    name=channel_name + "_1",
    loc=cq.Location((210.5, 0, 21.35), (0, 0, 1), 90),
)
result.add(
    channel,
    name=channel_name + "_2",
    loc=cq.Location((210.5, 0, 26.35), (0.71, -0.71, 0), 180),
)
#   - quad block mounts
result.add(
    qbm,
    name=qbm_name + "_bottom_rear",
    loc=cq.Location((-29.5, 0, 0), (0, 0, -1), 90),
)
result.add(
    qbm,
    name=qbm_name + "_bottom_front",
    loc=cq.Location((210.5, 0, 0), (0, 0, 1), 90),
)
result.add(
    qbm,
    name=qbm_name + "_top_rear",
    loc=cq.Location((-29.5, 0, 48.0), (0, 0, -1), 90),
)
result.add(
    qbm,
    name=qbm_name + "_top_front",
    loc=cq.Location((210.5, 0, 48.0), (0, 0, 1), 90),
)
#   - standoffs
result.add(
    standoff,
    name=standoff_name + "_bottom_rear",
    loc=cq.Location((58.5, 0, -16.2), (0, 0, 1), 0),
)
result.add(
    standoff,
    name=standoff_name + "_bottom_front",
    loc=cq.Location((122.5, 0, -16.2), (0, 0, 1), 0),
)
result.add(
    standoff,
    name=standoff_name + "_top_rear",
    loc=cq.Location((18.5, 0, 63.8), (0, 0, 1), 0),
)
result.add(
    standoff,
    name=standoff_name + "_top_front",
    loc=cq.Location((162.5, 0, 63.8), (0, 0, 1), 0),
)
#   - central wheel
result.add(
    wheel,
    name=wheel_name,
    loc=cq.Location((90.5, 12.0, 48.0), (1, 0, 0), 90),
)
#   - hyper hub
result.add(
    hyper_hub,
    name=hyper_hub_name,
    loc=cq.Location((-26.5, 5.75, 15.375), (0, 1, 0), -90),
)
#   - center wheel axle
result.add(
    shaft6,
    name=shaft6_name,
    loc=cq.Location((90.5, -35.0, 48.0), (0, 0, 1), 0),
)

# - prepare symmetrical parts
#   - channels
next_face = channel.faces(">X[1]").val()
punctured_channel = (
    channel.faces(">X")
    .workplane(centerOption="CenterOfMass")
    .circle(9.0)
    .cutBlind(next_face)
)
next_face = punctured_channel.faces("<X[1]").val()
punctured_channel = (
    punctured_channel.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .move(0.0, -48.0)
    .circle(35.0)
    .cutBlind(next_face)
)

# - add symmetrical parts
symm = cq.Assembly(name="hip_symmetrical")
#   - channel
symm.add(
    punctured_channel,
    name=channel_name + "_side",
    loc=cq.Location((210.5, -48.0, 69.35), (0, 0, 1), 90),
)
#   - quad block mounts
symm.add(
    qbm,
    name=qbm_name + "_side_rear",
    loc=cq.Location((-29.5, -48.0, 48.0), (0, 0, -1), 90),
)
symm.add(
    qbm,
    name=qbm_name + "_side_front",
    loc=cq.Location((210.5, -48.0, 48.0), (0, 0, 1), 90),
)
#   - side channel
symm.add(
    side_channel,
    name=side_channel_name,
    loc=cq.Location((26.5, -96.0, 69.35), (0, 0, 1), 90),
)
#   - standoffs
symm.add(
    standoff,
    name=standoff_name + "_side_rear",
    loc=cq.Location((42.5, -48.0, 31.8), (0, 0, 1), 0),
)
symm.add(
    standoff,
    name=standoff_name + "_side_front",
    loc=cq.Location((138.5, -48.0, 31.8), (0, 0, 1), 0),
)
# servo assembly
#   - servo mount
symm.add(
    servo_mount,
    name=servo_mount_name,
    loc=cq.Location((-20.0, -63.5 - 48.0, 7.0), (0.58, -0.58, -0.58), 240),
)
#   - servo
symm.add(
    servo_hs488hb,
    name=servo_hs488hb_name,
    loc=cq.Location((-46.3, -57.9 - 48.0, 38.0), (0.58, 0.58, -0.58), 120),
)
# center wheel axle
#   - bearing 6mm
symm.add(
    bearing6,
    name=bearing6_name,
    loc=cq.Location((90.5, -20.0, 48.0), (0, 0, 1), 180),
)
#   - collar 6mm
symm.add(
    collar6,
    name=collar6_name,
    loc=cq.Location((149.75, -39.0, 23.2), (0, 0, 1), 0),
)
# mounting for a thigh
#   - hyper hub
symm.add(
    hyper_hub,
    name=hyper_hub_name + "_side",
    loc=cq.Location((84.75, -21.0, 15.375), (-0.58, 0.58, -0.58), 240),
)

# vision assembly
vision = cq.Assembly(name="vision_assembly")
#   - beams
vision.add(
    beam,
    name=beam_name + "_1",
    loc=cq.Location((-4.0, -36.25, -71.75), (0.0, 0.0, 1.0), 0),
)
vision.add(
    beam,
    name=beam_name + "_2",
    loc=cq.Location((-36.0, -36.25, -71.75), (0.0, 0.0, 1.0), 0),
)
#   - servo mount
vision.add(
    servo_mount,
    name="vision_" + servo_mount_name,
    loc=cq.Location((-35.6, -21.25, -63.5), (0.58, -0.58, 0.58), 240),
)
#   - servo
vision.add(
    servo_hs488hb,
    name="vision_" + servo_hs488hb_name + "_1",
    loc=cq.Location((-10.0, 9.75, -98.0), (0.58, 0.58, 0.58), 120),
)
#   - servo attachment
vision.add(
    servo_attachment,
    name="vision_" + servo_attachment_name,
    loc=cq.Location((-20.0, -0.25, -53.0), (-1.0, 0.0, 0.0), 90),
)
vision2 = cq.Assembly(name="vision_1dof_assembly")
#   - servo mount
vision2.add(
    servo_mount,
    name="vision_1dof_" + servo_mount_name,
    loc=cq.Location((1.0, 11.5, -39.5), (0.0, 0.0, 1.0), 0),
)
#   - servo
vision2.add(
    servo_hs488hb,
    name="vision_1dof_" + servo_hs488hb_name + "_1",
    loc=cq.Location((-30.0, 46.0, -14.0), (0.0, 0.0, 1.0), 180),
)
vision3 = cq.Assembly(name="vision_2dof_assembly")
#   - servo arm attachment
vision3.add(
    servo_arm_attachment,
    name="vision_2dof_" + servo_arm_attachment_name,
    loc=cq.Location((-32.0, -2.0, -24.0), (0.0, 0.71, 0.71), 180),
)
#   - camera channel
vision3.add(
    camera_channel,
    name="vision_2dof_" + camera_channel_name,
    loc=cq.Location((-7.5, 48.0, -2.5), (0.0, 0.0, 1.0), 180),
)
vision2.add(
    vision3,
    loc=cq.Location((12.0, 0.0, 0.0), (0.0, 0.0, 1.0), 0),
)
vision.add(
    vision2,
    loc=cq.Location((-4.0, -8.0, -8.0), (0.0, 0.0, 1.0), 0),
)
symm.add(
    vision,
    loc=cq.Location((142.5, -151.75, 135.75), (0.0, 0.0, 1.0), 0),
)

result.add(symm)
symm_shape = symm.toCompound()
result.add(symm_shape.mirror(mirrorPlane="XZ"))

connect = cq.Assembly(name="connect_assembly")
result.add(connect)

disconnect = cq.Assembly(name="disconnect_assembly")
result.add(disconnect)

if __name__ == "__main__":
    shape = result.toCompound()

    try:
        ov.config.status()
        print("Visualizing...")
        ov.show(shape)
    except:
        print('No VS Code or "OCP CAD Viewer" extension detected.')

    print("Generating STL...")
    shape.exportStl(
        models + "/../platform/src/openvmp_robot_don1/meshes/hip.stl", 0.5, 5.0
    )
    print("Generating OBJ...")
    exportOBJ(shape, models + "/../platform/src/openvmp_robot_don1/meshes/hip.obj")

    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    print("Generating SVG...")
    cq.exporters.export(
        shape,
        models + "/generated_files/robots/don1/hip.svg",
        opt=exportSvgOpts,
    )

    print("Generating PNG...")
    cairosvg.svg2png(
        url=models + "/generated_files/robots/don1/hip.svg",
        write_to=models + "/generated_files/robots/don1/hip.png",
        output_width=exportSvgOpts["width"],
        output_height=exportSvgOpts["height"],
    )

else:
    show_object(
        result,
        options={
            "parts": bom.self_parts,
            "name": "body_link",
        },
    )
