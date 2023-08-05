import sys
import cadquery as cq

if len(sys.argv) < 2:
    print("Usage: python3 " + sys.argv[0] + " <STEP-file>")
    sys.exit(1)

path = sys.argv[1]
result = cq.importers.importStep(path)
cq.exporters.export(result, path, cq.exporters.ExportTypes.STEP, opt={"write_pcurves": False})
