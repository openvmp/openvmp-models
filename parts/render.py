import cadquery as cq
from glob import glob
import json
import os
import os.path
import sys

sys.path.append(".")
from lib.bom import Bom
from lib.doc import exportSvgOpts

titles = {
    "custom": "Custom OpenVMP parts",
    "gobilda": "OpenVMP parts from [goBILDA](https://www.gobilda.com/)",
    "stepperonline": "OpenVMP parts from [STEPPERONLINE](https://stepperonline.com/)",
}
descriptions = {
    "custom": "This folder conatins parts that must be custom made specifically for OpenVMP.",
    "gobilda": "This folder contains parts that can be purchased from [goBILDA](https://www.gobilda.com/).",
    "stepperonline": "This folder contains parts that can be purchased from [STEPPERONLINE](https://stepperonline.com/).",
}

# Walk through all sub-folders.
folders = glob("parts/*")
for folder in folders:
    if not os.path.isdir(folder):
        continue
    folder_dir = os.path.basename(folder)
    print("Iterating over " + folder_dir + "...")

    parts = []
    paths = glob(folder + "/*")
    for path in paths:
        if not os.path.isdir(path):
            continue
        dir = os.path.dirname(path)
        part_basename = os.path.basename(path)

        part = json.loads(open(path + "/part.json").read())

        print("Loading " + path + "...")
        bom = Bom()
        result = cq.Assembly()
        bom.add_part(result, path)

        shape = result.toCompound()
        shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

        print("Exporting " + path + " to STL...")
        shape.exportStl("generated_files/" + path + ".stl", 0.2, 1.0)

        print("Exporting " + path + " to SVG...")
        cq.exporters.export(
            shape,
            "generated_files/" + path + ".svg",
            opt=exportSvgOpts,
        )

        print("Generating README.md in " + path + "...")
        if "url" in part:
            desc = "[" + part["desc"] + "](" + part["url"] + ")"
        else:
            desc = part["desc"]
        readme = ""
        if "readme" in part:
            readme = part["readme"]

        contents = (
            "# "
            + titles[folder_dir]
            + "\n"
            + "## "
            + desc
            + "\n\n"
            + "[<img alt='"
            + part["desc"]
            + "' src='https://github.com/openvmp/openvmp-models/blob/main/generated_files/parts/"
            + folder_dir
            + "/"
            + part_basename
            + ".svg'/>](https://github.com/openvmp/openvmp-models/blob/main/generated_files/parts/"
            + folder_dir
            + "/"
            + part_basename
            + ".stl)\n\n"
            + readme
        )
        readme = open(path + "/README.md", "w+")
        readme.write(contents)
        readme.close()

        part["dir"] = dir
        part["path"] = path
        part["basename"] = part_basename
        parts.append(part)

    # Now sort the parts to keep the top level README's table normalized.
    parts = sorted(parts, key=lambda x: x["basename"])

    # Generate the README file in the top level folder.
    print("Generating README.md in the folder " + folder_dir + "...")
    contents = (
        "# "
        + titles[folder_dir]
        + "\n"
        + descriptions[folder_dir]
        + """

  See [openvmp-models](https://github.com/openvmp/openvmp-models) for more info.

  | Part | Image |
  | -- | -- |
  """
    )
    readme = open(folder + "/README.md", "w+")
    readme.write(contents)

    for part in parts:
        readme.write(
            "| ["
            + part["desc"]
            + "](./"
            + part["basename"]
            + ") | <img alt='"
            + part["desc"]
            + "' src='https://github.com/openvmp/openvmp-models/blob/main/generated_files/"
            + part["path"]
            + ".svg' width='300' /> |\n"
        )

    readme.close()
