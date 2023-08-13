# Don1

[<img alt="Don1" src="../../generated_files/robots/don1/robot.png"/>](../../generated_files/robots/don1/robot.stl)

This robot is smart, powerful and large (>1m long). It's made of goBILDA components, some off-the-shelf stainless steel sheets and 3D printed parts.
The bill of materials can be found [here](../../generated_files/robots/don1/bom.md).

It is designed to perform tasks on its own. But it also has enough computing power to control a fleet of smaller OpenVMP robots.

## High Level Architecture

The robot modules are separated from each other by 1 degree of freedom.

```mermaid
graph TB
  camera1 -.-> camera_servo1 -.-> hip1
  wheel1 -.-> foot1 -.-> thigh1 -.-> hip1
  wheel3 -...-> hip1 -.-> turntable1 -.-> base
  wheel2 -.-> foot2 -.-> thigh2 -.-> hip1
  camera2 -.-> camera_servo2 -.-> hip1

  camera3 -.-> camera_servo3 -.-> hip2
  wheel4 -.-> foot3 -.-> thigh3 -.-> hip2
  wheel6 -...-> hip2 -.-> turntable2 -.-> base
  wheel5 -.-> foot4 -.-> thigh4 -.-> hip2
  camera4 -.-> camera_servo4 -.-> hip2

  base(Base)
  click base "https://github.com/openvmp/openvmp-models/blob/main/generated_files/robots/don1/base.png" _blank
  turntable1(Turntable)
  click turntable1 "https://github.com/openvmp/openvmp-models/blob/main/generated_files/robots/don1/turn_table.png" _blank
  turntable2(Turntable)
  hip1(Hip)
  hip2(Hip)
  thigh1(Thigh)
  thigh2(Thigh)
  thigh3(Thigh)
  thigh4(Thigh)
  foot1(Foot)
  foot2(Foot)
  foot3(Foot)
  foot4(Foot)
  wheel1(Wheel)
  wheel2(Wheel)
  wheel3(Wheel)
  wheel4(Wheel)
  wheel5(Wheel)
  wheel6(Wheel)
  camera1(Camera)
  camera2(Camera)
  camera3(Camera)
  camera4(Camera)
  camera_servo1(Camera\nBase)
  camera_servo2(Camera\nBase)
  camera_servo3(Camera\nBase)
  camera_servo4(Camera\nBase)
```

## Modules

<img style="width: 50%; float:right;" align="right" alt="base" src=../../generated_files/robots/don1/base.png />

### Base

The base of the robot is where the battery and most of electronics are.
It has coupled motors to turn front and rear sides of the robot using turntables.

<br style="clear: right;" />
<img style="width: 50%; float:right;" align="right" alt="turn_table" src=../../generated_files/robots/don1/turn_table.png />

### Turntable

There is a turntable on each side of the robot.
It's being turned left and right by the base.
Turntable itself rotates the hip around it's center axle.

<br style="clear: right;" />
<img style="width: 50%; float:right;" align="right" alt="hip" src=../../generated_files/robots/don1/hip.png />

### Hip

The hip is connected to the turntable.
Each hip has a passive (no motor) wheel in the center and two thighs attached on each side.
It also has two camera bases attached on each side.
The only motors it has are servos to turn cameras and connect/disconnect mechanisms.

<br style="clear: right;" />
<img style="width: 50%; float:right;" alt=thigh src=../../generated_files/robots/don1/lower_arm.png />

### Thigh

The thigh has motors to both turn itself and to bend the knee.

<br style="clear: right;" />
<img style="width: 50%; float:right;" alt=foot src=../../generated_files/robots/don1/upper_arm.png />

### Foot

The foot has a motor to drive the wheel.
It also has mechanical parts to aid various ways of movement:
pushing, grabbing etc.

<br style="clear: right;" />
<img style="width: 60%; float:right;" alt=foot src=../../generated_files/robots/don1/camera_servo.png />

### Camera Base

This is the lower moving part of the camera assembly.
It hosts the second servo that adds the second degree of freedom to the camera.

<br style="clear: right;" />
<img style="width: 60%; float:right;" alt=foot src=../../generated_files/robots/don1/camera.png />

### Camera

This is the housing for the stereo camera assembly.

<br style="clear: right;" />
<img style="width: 60%; float:right;" alt=foot src=../../generated_files/robots/don1/wheel.png />

### Wheel

This wheel provides the grip the robot needs to climb up.
