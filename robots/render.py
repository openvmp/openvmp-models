import concurrent.futures
from glob import glob
import os
import sys

pids_pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count())

def robot_thread(path):
    child_pid = os.fork()
    if child_pid == 0:
        os.execv(sys.executable, ["python3", path])
    else:
        os.waitpid(child_pid, 0)

paths = glob("robots/*/*.py")
for path in paths:
    print("Rendering " + path + "...")
    pids_pool.submit(robot_thread, path)

pids_pool.shutdown(wait=True)
