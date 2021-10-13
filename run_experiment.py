from randomsequencefuzzerwithfixedparams import RandomSequenceFuzzerWithFixedParams
from randomsequencefuzzerwithfixedparamsandexacttypes import RandomSequenceFuzzerWithFixedParamsAndExactTypes
from randomcommandsequencefuzzer import RandomCommandsSequenceFuzzer
from randomsequencefuzzer import RandomSequenceFuzzer
from flightsoftwarerunner import FlightSoftwareRunner
from subprocess import PIPE, Popen
import os
import pandas as pd
import json
import time
import argparse


def to_json(information, iterations, t, json_path):
    """
    Write information to JSON file.
    :param information: Tuple with list of commands, list of parameters, executed commands, command results,
            commands execution time, exit code of the process, total execution time, real memory used and
            virtual memory used
    :param iterations: Int.
    :param t: String. Start date and time of the execution.
    :return:
    """
    json_lst = []
    for i in range(iterations):
        iter_dic = dict()

        # Add information of each command sent
        cmds_lst = []
        results = information[i]
        cmds_sent = results[0]
        params_sent = results[1]
        for j in range(len(cmds_sent)):
            cmds_lst.append({"cmd_name": cmds_sent[j], "params": params_sent[j]})
        iter_dic['cmds'] = cmds_lst

        # Add general information of the sequence
        iter_dic['exit code'] = results[5]
        iter_dic['total time (s)'] = results[6]  # Select a sequence, then the results of it, then the time
        iter_dic['virtual memory (kb)'] = results[8]
        iter_dic['real memory (kb)'] = results[7]
        json_lst.append(iter_dic)

    # Write to json
    filename = 'data-' + t + '.txt'
    if not os.path.exists(json_path):
        os.mkdir(json_path)
    with open(json_path + filename, 'w') as outfile:
        json.dump(json_lst, outfile, indent=2, separators=(',', ': '))


def to_csv_file(information, iterations, t, csv_path):
    """
    Write information to CSV file.
    :param information: Tuple with list of commands, list of parameters, executed commands, command results,
            commands execution time, exit code of the process, total execution time, real memory used and
            virtual memory used
    :param iterations: Int.
    :param t: String. Start date and time of the execution.
    :return:
    """
    information_list = []
    for i in range(iterations):
        information_list.append([])
        results = information[i]
        cmds_sent = results[0]
        params_sent = results[1]
        for j in range(len(cmds_sent)):
            information_list[i].append(cmds_sent[j])
            information_list[i].append("'" + params_sent[j] + "'")
        information_list[i].append(results[5])
        information_list[i].append(results[6])
        information_list[i].append(results[8])
        information_list[i].append(results[7])

    cols = []
    for k in range(len(information[0][0])):
        cols.append("Command")
        cols.append("Parameters")
    cols.append("Exit Code")
    cols.append("Total Time")
    cols.append("Virtual Memory (kB)")
    cols.append("Real Memory (kB)")

    information_df = pd.DataFrame(information_list, columns=cols)
    filename = 'data-' + t + '.csv'
    if not os.path.exists(csv_path):
        os.mkdir(csv_path)
    information_df.to_csv(csv_path + filename, index=False)


def run_experiment(iterations=10, cmds_number=10, csv_path='', json_path=''):
    """
    Create a random fuzzer instance to execute flight software with random input.
    :param iterations: Int.
    :param cmds_number: Int. Number of commands to execute each iteration.
    :return:
    """
    print("Commands number: " + str(cmds_number) + ", iteration: " + str(iterations))

    # Get lists of all the flight software commands, and number of parameters that each one receives
    fs_cmds = []
    #params_type = []  # Fixed number of parameters and exact types
    #number_of_params = [] # Fixed number of parameters
    # with open("suchai_cmd_list_excluded_bugs.csv") as f:
    #with open("suchai_cmd_list_all.csv") as f:  # in this file 4 commands were excluded (log_set obc_reset obc_set_time obc_system)
    with open("suchai_cmd_list_ba186c9a994af2564c55e3aaac4cb07b3619361d-GND.csv") as f: # in this file 4 commands were excluded (log_set obc_reset obc_set_time obc_system) and unnecessary commands
        for row in f:
            fs_cmds.append(row.split(', ')[0])
            #params_str_without_newline = row.rstrip('\n')  # Fixed number of parameters and exact types
            #params_type.append(params_str_without_newline.split(', ')[2:])  # Fixed number of parameters and exact types
            #number_of_params.append(int(row.split(', ')[1]))  # Fixed number of parameters
    # print(params_type)
    # Run zmqhub.py (ipc)
    # ex_zmqhub = Popen(["python3", "zmqhub.py", "--ip", "/tmp/suchaifs", "--proto", "ipc"], stdin=PIPE)
    # Run zmqhub.py (tcp)
    ex_zmqhub = Popen(["python3", "zmqhub.py", "--mon"], stdin=PIPE)

    # Set variables
    exec_dir = "../../Git/suchai-flight-software4/build_groundstation/"
    exec_cmd = "./SUCHAI_Flight_Software"
    # Fixed number of parameters (Strategy 2)
    #random_fuzzer = RandomSequenceFuzzerWithFixedParams(number_of_params=number_of_params, min_length=0,
    #                                     max_length=10, char_start=33, char_range=93, n_cmds=cmds_number,
    #                                                    fs_cmds=fs_cmds)

    # Fixed number of parameters and exact types (Strategy 3)
    #random_fuzzer = RandomSequenceFuzzerWithFixedParamsAndExactTypes(params_types=params_type, min_length=0,
    #                                                                 max_length=10, char_start=33, char_range=93,
    #                                                                 n_cmds=cmds_number, fs_cmds=fs_cmds)

    #Random number of parameters and random types (Strategy 1)
    random_fuzzer = RandomSequenceFuzzer(min_length=0, max_length=10, char_start=33, char_range=93, n_cmds=cmds_number,
                                         fs_cmds=fs_cmds)

    # Random commands (Strategy 0)
    #random_fuzzer = RandomCommandsSequenceFuzzer(min_length=0, max_length=10, n_cmds=cmds_number)

    prev_dir = os.getcwd()

    # Run flight software sending n_cmds random commands with 1 random parameter
    os.chdir(exec_dir)
    start_time = time.strftime("%Y%m%d-%H%M%S")  # Measure start time to include it in the report name
    outcomes = random_fuzzer.runs(FlightSoftwareRunner(exec_cmd=exec_cmd), iterations)

    os.chdir(prev_dir)

    # Kill zmqhub.py
    ex_zmqhub.kill()

    # Write outcome information report
    to_json(outcomes, iterations, start_time, json_path)

    # Write report to csv file
    to_csv_file(outcomes, iterations, start_time, csv_path)


def get_parameters():
    """
    Parse script arguments
    """
    parser = argparse.ArgumentParser(prog='run_experiment.py')

    #parser.add_argument('--csv_path', type=str, default='CSV-reports/After-Fix-12/Strategy1/')
    #parser.add_argument('--json_path', type=str, default='JSON-reports/After-Fix-12/Strategy1/')
    #parser.add_argument('--time_path', type=str, default='Execution-time/After-Fix-12/Strategy1/')
    parser.add_argument('--csv_path', type=str, default='CSV-reports/Commit-ba186c9a994af2564c55e3aaac4cb07b3619361d-GND/Strategy1/')
    parser.add_argument('--json_path', type=str, default='JSON-reports/Commit-ba186c9a994af2564c55e3aaac4cb07b3619361d-GND/Strategy1/')
    parser.add_argument('--time_path', type=str, default='Execution-time/Commit-ba186c9a994af2564c55e3aaac4cb07b3619361d-GND/Strategy1/')

    return parser.parse_args()


def main(time_path, csv_path, json_path):
    iters_list = [1000]#[10, 100, 500, 1000]
    n_cmds_list = [5]  #[5, 10, 50, 100]

    # Create file to write execution time for each iteration
    curr_time = time.strftime("%Y%m%d-%H%M%S")

    if not os.path.exists(time_path):
        os.mkdir(time_path)

    f = open(time_path + 'exec_time-' + curr_time + '.txt', '+w')
    f.close()

    # Run iterations and add execution time to file
    for num_cmds in n_cmds_list:
        for iter in iters_list:
            exec_start_time = time.time()
            run_experiment(iter, num_cmds, csv_path, json_path)
            with open(time_path + 'exec_time-' + curr_time + '.txt', 'a') as f:
                f.write("%s\n" % (time.time() - exec_start_time))


if __name__ == "__main__":
    args = get_parameters()
    main(args.time_path, args.csv_path, args.json_path)



