import pandas as pd
from os import listdir
import json

strategy0_path = '/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/JSON-reports/Strategy0/'
strategy1prev_path = '/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/CSV-reports/Strategy1-prev/'
strategy1_path = '/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/CSV-reports/Strategy1/'
strategy2_path = '/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/CSV-reports/Strategy2/'
strategy3_path = '/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/CSV-reports/Strategy3/'

strategy0_results_files = [f for f in listdir(strategy0_path)]
strategy1prev_results_files = [f for f in listdir(strategy1prev_path)]
strategy1_results_files = [f for f in listdir(strategy1_path)]
strategy2_results_files = [f for f in listdir(strategy2_path)]
strategy3_results_files = [f for f in listdir(strategy3_path)]


# CSV
"""for file in strategy0_results_files:
    path = 'CSV-reports/Strategy0/' + file
    results = pd.read_csv(path)
    total_cols = 1
    for col in results.columns:
        if col == "Command." + str(total_cols):
            total_cols += 1
    total_rows = results["Exit Code"].count()
    fail_execs_number = results.loc[results["Exit Code"] != 0]["Exit Code"].count()
    failure_percentage = (fail_execs_number/total_rows) * 100.0
    max_real_memory = results["Real Memory (kB)"].max()
    with open("matrix_strat0.txt", "a") as f:
        f.write(str(total_rows) + " iterations and " + str(total_cols) + " commands: " + str(failure_percentage) +
                "% of failure" + ", " + str(max_real_memory) + " kB of max. real memory used\n")
    print(failure_percentage)"""

#JSON
for file in strategy0_results_files:
    path = 'JSON-reports/Strategy0/' + file
    with open(path) as results_file:
        file_json = json.load(results_file)
        total_rows = len(file_json)  # Data size
        total_cols = len(file_json[0]["cmds"])  # Number of commands sent
        fail_execs_number = len([1 for dic in file_json if dic["exit code"] != 0])
        failure_percentage = (fail_execs_number/total_rows) * 100.0
        max_real_memory = max([dic["real memory (kb)"] for dic in file_json])
        with open("matrix_strat0.txt", "a") as f:
            f.write(str(total_rows) + " iterations and " + str(total_cols) + " commands: " + str(failure_percentage) +
                    "% of failure" + ", " + str(max_real_memory) + " kB of max. real memory used\n")

