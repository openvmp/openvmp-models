import cadquery as cq
from glob import glob
import os.path
import sys

sys.path.append(".")
from lib.bom import Bom

paths = glob("parts/*/*")
for path in paths:
    if not os.path.isdir(path):
        continue

    print("Rendering " + path + "...")

    bom = Bom()
    result = cq.Assembly()
    bom.add_part(result, path)

    shape = result.toCompound()
    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)

    cq.exporters.export(
        shape,
        "generated_files/" + path + ".svg",
        opt={
            "width": 500,
            "height": 200,
            "marginLeft": 12,
            "marginTop": 12,
            "showAxes": False,
            "projectionDir": [0.5, 0.25, 0.5],
            "strokeWidth": 0.25,
            "strokeColor": [64, 255, 64],
            "hiddenColor": [32, 64, 32],
            "showHidden": False,
        },
    )
