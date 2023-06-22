# Don1

[<img alt="Don1" src="../../generated_files/robots/don1/robot.png"/>](../../generated_files/robots/don1/robot.stl)

This robot is smart, powerful and large (>1m long). It's made of goBILDA components, some off-the-shelf stainless steel sheets and 3D printed parts.
The bill of materials can be found [here](../../generated_files/robots/don1/bom.md).

It is designed to perform tasks on its own. But it also has enough computing power to control a fleet of smaller OpenVMP robots.


## High Level Architecture

The major modules are separated from each other by 1 degree of freedom.


```mermaid
graph TB
  foot1 -.-> thigh1 -.-> hip1
  foot2 -.-> thigh2 -.-> hip1
  foot3 -.-> thigh3 -.-> hip2
  foot4 -.-> thigh4 -.-> hip2
  hip1 -.-> turntable1 -.-> base
  hip2 -.-> turntable2 -.-> base

  base(" ")
  classDef classNameBase height:80px,min-width:200px;background-image:url(https://github.com/openvmp/openvmp-models/blob/main/generated_files/robots/don1/base.png);
  class base classNameBase;
  click base "https://github.com/openvmp/openvmp-models/blob/main/generated_files/robots/don1/base.stl" _blank
  turntable1("<img height=80 alt=turn_table style='min-width:200px' src='https://github.com/openvmp/openvmp-models/blob/main/generated_files/robots/don1/turn_table.png' />")
  click turntable1 "https://github.com/openvmp/openvmp-models/blob/main/generated_files/robots/don1/turn_table.stl" _blank
  turntable2(<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=turn_table style='min-width:200px' src=../../generated_files/robots/don1/turn_table.png /></a>)
  hip1("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=hip style='min-width:200px' src=../../generated_files/robots/don1/hip.png /></a>")
  hip2("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=hip style='min-width:200px' src=../../generated_files/robots/don1/hip.png /></a>")
  thigh1("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=thigh style='min-width:200px' src=../../generated_files/robots/don1/lower_arm.png /></a>")
  thigh2("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=thigh style='min-width:200px' src=../../generated_files/robots/don1/lower_arm.png /></a>")
  thigh3("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=thigh style='min-width:200px' src=../../generated_files/robots/don1/lower_arm.png /></a>")
  thigh4("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=thigh style='min-width:200px' src=../../generated_files/robots/don1/lower_arm.png /></a>")
  foot1("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=foot style='min-width:200px' src=../../generated_files/robots/don1/upper_arm.png /></a>")
  foot2("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=foot style='min-width:200px' src=../../generated_files/robots/don1/upper_arm.png /></a>")
  foot3("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=foot style='min-width:200px' src=../../generated_files/robots/don1/upper_arm.png /></a>")
  foot4("<a href='../../generated_files/robots/don1/base.stl'><img height=80 alt=foot style='min-width:200px' src=../../generated_files/robots/don1/upper_arm.png /></a>")
```

## Modules

### Base

<img height=240 alt=base style='min-width: 600px' src=../../generated_files/robots/don1/base.png />

The base of the robot is where the battery and computers are.
It has coupled motors to turn front and rear sides using turntables to left and right.

### Turntable

<img height=240 alt=turn_table style='min-width:600px' src=../../generated_files/robots/don1/turn_table.png />

Turntable is on each side of the robot to rotate the hip around it's own axle.

### Hip

<img height=240 alt=hip style='min-width:600px' src=../../generated_files/robots/don1/hip.png />

The hip is connected to the turntable. Thighs are attached to each side.
It only has motors to turn cameras and connect/disconnect mechanisms.

### Thigh

<img height=240 alt=thigh style='min-width:600px' src=../../generated_files/robots/don1/lower_arm.png />

The thigh has motors to both turn itself and to bend the knee.

### Foot

<img height=240 alt=foot style='min-width:600px' src=../../generated_files/robots/don1/upper_arm.png />

The foot has a motor to drive the wheel.
It also has mechanical parts to aid various ways of movement:
pushing, grabbing etc.
