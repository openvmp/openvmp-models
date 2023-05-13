# CAD models for [OpenVMP robots](https://github.com/openvmp/openvmp/) [WORK-IN-PROGRESS]

This package is an optinal part of [the OpenVMP project](https://github.com/openvmp/openvmp). It is only required for hardware design and manufacturing/assembly activities.

## Introduction

This submodule serves two purposes:

- generate images and 3D models for robot simulations and documentation
- generate bill of materials (with building and ordering instructions)

This submodule contains large files by design
and it's not required for most of use cases.
That's why it is moved to a separate repository.

## Images and 3D models

[The main OpenVMP repository](https://github.com/openvmp/openvmp/)
already contains all the necessary images and 3D models.
However, as OpenVMP robots evolve and improve,
all these files need to be regenerated.

Whenever the part files change, run `python3 ./parts/render.py`
to generate updated part images. Run `python3 ./robots/render.py`
to render images and STL files, including images and mesh files in `../platform/src/openvmp_robot_<...>`.

## Bill of materials

OpenVMP can generate the bill of materials for each robot.
For example, the bill of materials for Don1 can be printed
by running `./models/robots/don1/bom.py`.

## Robot CAD models

| Robot                    | Preview                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| [Don1](./don1/README.md) | <img alt="Don1" style="background-color: black;" src="./generated_files/robots/don1/robot.svg"/> |

- [robots](./robots/README.md): CAD models and assembly instructions
for whole robots

## Robot parts

CAD models and manufacturing/ordering instructions can be found [here](./parts/README.md).

### Troubleshooting CadQuery

Use `.` as the current folder for all CadQuery command line sessions.

In a terminal window, run `cd models && cq-server run <path>`,
where `path` is either `robot/<robot_name>` or `parts/<type>/<part>`.

In VS Code, use a 'SimpleBrowser' view to open `http://127.0.0.1:5000/`
(to connect to `cq-server`).
Also, see the rendered SVG files in the markdown preview views.
