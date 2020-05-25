import pandas as pd
from os import listdir
strategies = ["1", "2", "3"]
csv_reports_path = '/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/CSV-reports'

for strat in strategies:
    strat_files_list = [f for f in listdir(csv_reports_path + '/Strategy' + strat)]
    for file in strat_files_list:
        path = csv_reports_path + '/Strategy' + strat + '/' + file
        results = pd.read_csv(path)
        final_df = results[results["Exit Code"] != 0]
        final_df = final_df.drop(columns=["Virtual Memory (kB)", "Real Memory (kB)"])
        final_df.to_csv("Strategy" + strat + "/" + strat + file, index=False)
