from randomsequencefuzzer import RandomSequenceFuzzer
from flightsoftwarerunner import FlightSoftwareRunner
from subprocess import PIPE, Popen
import os
import time
import json


def to_json(information, iterations):
    json_lst = []
    for i in range(iterations):
        iter_dic = dict()

        # Add information of each command sent
        cmds_lst = []
        results = information[i][0]
        cmds_sent = results[0]
        params_sent = results[1]
        for j in range(len(cmds_sent)):
            cmds_lst.append({"cmd_name": cmds_sent[j], "params": params_sent[j]})
        iter_dic['cmds'] = cmds_lst

        # Add general information of the sequence
        iter_dic['exit code'] = information[i][0][5]
        iter_dic['total time'] = information[i][0][6]  # Select a sequence, then the results of it, then the time
        iter_dic['virtual memory'] = information[i][0][8]
        iter_dic['real memory'] = information[i][0][7]
        json_lst.append(iter_dic)

    # Write to json
    with open('/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/data.txt', 'w') as outfile:
        json.dump(json_lst, outfile, indent=2, separators=(',', ': '))


if __name__ == "__main__":
    # Run zmqhub.py
    ex_zmqhub = Popen(["python3", "zmqhub.py"], stdin=PIPE)

    # Set variables
    exec_dir = "../../Git/SUCHAI-Memoria/build_x86/"
    exec_cmd = "./SUCHAI_Flight_Software"
    random_fuzzer = RandomSequenceFuzzer(min_length=1, max_length=1, char_start=ord('0'), char_range=10, n_cmds=2)

    # Run flight software sending 5 random commands with 1 random parameter
    iter = 3  # Number of iterations for the experiment
    os.chdir(exec_dir)
    outcomes = random_fuzzer.runs(FlightSoftwareRunner(exec_cmd=exec_cmd), iter)

    # Kill zmqhub.py
    ex_zmqhub.kill()

    # Write outcome information report
    to_json(outcomes, iter)
