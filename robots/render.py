from glob import glob
import os

paths = glob("robots/*/*.py")
for path in paths:
    print("Rendering " + path + "...")
    os.system("python3 " + path)
