import cadquery as cq
import partcad as pc

channel = pc.get_part_cadquery("structure/u_channel_9", "pc-robotics-gobilda")

channel = cq.Workplane(obj=channel)

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

show_object(punctured_channel)