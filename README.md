# CAD models of [OpenVMP robots](https://github.com/openvmp/openvmp/)

**Disclaimer**: This is a work in progress. Volunteers wanted to translate the existing FreeCAD models as well as photos of the real robot into CadQuery (Python) scripts.
 If you want to learn and practice CadQuery and help the community at the same time, please, reach out to [openvmp@proton.me](openvmp@proton.me).

## Introduction

This repository contains detailed blueprints of
[OpenVMP](https://github.com/openvmp/openvmp) robots.
Since it contains large files by design
and it's not required in most cases,
this repository is kept as a separate optional submodule.

This repository contains [the catalog of all parts](./parts/), how they look, how they can be manufactured or where they can be purchased. It also contains CadQuery scripts that codify [the blueprints of entire robots](./robots/), instructions how individual parts come together to form the robot.

| Robot                  | Preview                                                                                                    |
| ---------------------- | ---------------------------------------------------------------------------------------------------------- |
| [Don1](./robots/don1/) | [<img alt="Don1" src="./generated_files/robots/don1/robot.svg"/>](./generated_files/robots/don1/robot.stl) |

The default behavior of CadQuery scripts is extended to gerentate the following:

- images and 3D models
- bill of materials
### Images and 3D models

[The main OpenVMP repository](https://github.com/openvmp/openvmp/)
already contains all the necessary images and 3D models.
However, as OpenVMP robots evolve and improve,
all these files need to be regenerated to be rendered in documentation files and in simulation environments.

### Bill of materials

OpenVMP can generate the bill of materials for each robot to make
purchasing and inventorying easier.
For example, the bill of materials for Don1 can be found in
[./generated_files/robots/don1/bom.md](./generated_files/robots/don1/bom.md).

## Getting Started

### Rendering from command line

*Note: Use the top level of this repository (e.g. the `models` sub-folder of [the OpenVMP monorepo](https://github.com/openvmp/openvmp/)) as the current folder for all CadQuery command line sessions.*

Whenever the blueprints change, run `python3 ./parts/render.py`
to generate updated part images. Run `python3 ./robots/render.py`
to render robot images and STL files, including images and mesh files in `../platform/src/openvmp_robot_*`.

### Editing models in Visual Studio Code

In a terminal window, run `cd models && cq-server run <path>`,
where `path` is either `robots/<robot_name>` or `parts/<category>/<part>`.

In VS Code, use the 'SimpleBrowser' extension to navigate to
`http://127.0.0.1:5000/`
(to connect to the default port exposed by `cq-server`).

Also, the rendered SVG files can be seen in the markdown preview views.

### Editing models in CadQuery Editor

```
cd models && CQ-editor robots/<robot_name>/robot.py
```