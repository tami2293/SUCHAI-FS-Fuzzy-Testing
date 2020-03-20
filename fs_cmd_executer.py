import os
from subprocess import Popen, PIPE
from experiments import *


# Change the working directory
working_dir = os.getcwd()

fs_dir = "../../Git/SUCHAI-Memoria/"
exec_dir = "build_x86"
compilation_cmd = "python3 compile.py LINUX X86 --hk 0 --st_mode 2 --drivers"
exec = "./SUCHAI_Flight_Software"

# Run zmqhub.py
ex_zmqhub = Popen(["python3", "zmqhub.py"], stdin=PIPE)

os.chdir(fs_dir)
# os.system(compilation_cmd)  # Comment this if you don't need to compile the software
os.chdir(exec_dir)
# time.sleep(1)
suchai_process = Popen([exec], stdin=PIPE)
# time.sleep(1)

# Experiments
parm_type_fail(suchai_process, 5)

ex_zmqhub.kill()
