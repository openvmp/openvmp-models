import cadquery as cq
import cairosvg
from glob import glob
import json
import concurrent.futures
import os
import os.path
import sys

sys.path.append("models")
sys.path.append("..")
sys.path.append(".")
from lib.common import get_models_dir

models = get_models_dir()
os.chdir(models)

titles = {
    "custom": "Custom OpenVMP parts",
    "dfrobot": "OpenVMP parts from [DFRobot](https://www.dfrobot.com/)",
    "gobilda": "OpenVMP parts from [goBILDA](https://www.gobilda.com/)",
    "stepperonline": "OpenVMP parts from [STEPPERONLINE](https://stepperonline.com/)",
    "cloudray": "OpenVMP parts from [Cloudray](https://cloudray.com/)",
    "arduino": "OpenVMP parts from [Arduino](https://arduino.cc/)",
    "intel": "OpenVMP parts from [Intel](https://intel.com/)",
    "raspberry-pi": "OpenVMP parts from [Raspberry Pi](https://raspberrypi.com/)",
    "ego": "OpenVMP parts from [EGO](https://egopowerplus.com/)",
}
descriptions = {
    "custom": "This folder conatins parts that must be custom made specifically for OpenVMP.",
    "dfrobot": "This folder contains parts that can be purchased from [DFRobot](https://www.dfrobot.com/).",
    "gobilda": "This folder contains parts that can be purchased from [goBILDA](https://www.gobilda.com/).",
    "stepperonline": "This folder contains parts that can be purchased from [STEPPERONLINE](https://stepperonline.com/).",
    "cloudray": "This folder contains parts that can be purchased from [Cloudray](https://cloudray.com/).",
    "arduino": "This folder contains parts that can be purchased from [Arduino](https://arduino.cc/).",
    "intel": "This folder contains parts that can be purchased from [Intel](https://intel.com/).",
    "raspberry-pi": "This folder contains parts that can be purchased from [Raspberry Pi](https://raspberrypi.com/).",
    "ego": "This folder contains parts that can be purchased from [EGO](https://egopowerplus.com/).",
}

pids_pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count())

parts = {}


def part_thread(path):
    child_pid = os.fork()
    if child_pid == 0:
        os.execv(sys.executable, ["python3", "parts/render_one.py", path])
    else:
        os.waitpid(child_pid, 0)


def part_process(folder_dir, path):
    pids_pool.submit(part_thread, path)

    dir = os.path.dirname(path)
    part_basename = os.path.basename(path)

    print("Loading " + path + "...")
    part = json.loads(open(path + "/part.json").read())

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
        + ".png'/>](https://github.com/openvmp/openvmp-models/blob/main/generated_files/parts/"
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
    parts[folder_dir].append(part)


def folder_process(folder):
    folder_dir = os.path.basename(folder)
    print("Iterating over " + folder_dir + "...")

    parts[folder_dir] = []
    paths = glob(folder + "/*")
    for path in paths:
        if not os.path.isdir(path):
            continue
        part_process(folder_dir, path)

    # Now sort the parts to keep the top level README's table normalized.
    parts[folder_dir] = sorted(parts[folder_dir], key=lambda x: x["basename"])

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

    for part in parts[folder_dir]:
        readme.write(
            "| ["
            + part["desc"]
            + "](./"
            + part["basename"]
            + ") | <img alt='"
            + part["desc"]
            + "' src='https://github.com/openvmp/openvmp-models/blob/main/generated_files/"
            + part["path"]
            + ".png' width='300' /> |\n"
        )

    readme.close()


# Walk through all sub-folders.
folders = glob("parts/*")
for folder in folders:
    if not os.path.isdir(folder):
        continue
    folder_process(folder)

# Wait for all render processes to get initiated
pids_pool.shutdown(wait=True)
