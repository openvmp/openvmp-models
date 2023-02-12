# CAD models for OpenVMP robots [WORK-IN-PROGRESS]

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

## Contents

- [robots](./robots/README.md): CAD models and assembly instructions
for whole robots
- [parts](./parts/README.md): CAD models and manufacturing/ordering instructions

## Development Hints

Use `.` as the current folder for all command line sessions.


### Troubleshooting CadQuery

In a terminal window, run `cd models && cq-server run <path>`,
where `path` is either `robot/<robot_name>` or `parts/<type>/<part>`.

In VS Code, use a 'SimpleBrowser' view to open `http://127.0.0.1:5000/`
(to connect to `cq-server`).
Also, see the rendered SVG files in the markdown preview views.
