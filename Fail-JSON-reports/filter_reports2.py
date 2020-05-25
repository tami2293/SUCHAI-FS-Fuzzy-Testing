from os import listdir
import json

strategies = ["1", "2", "3"]
csv_reports_path = '/home/tamara/Git/SUCHAI-FS-Fuzzy-Testing/JSON-reports'

for strat in strategies:
    strat_files_list = [f for f in listdir(csv_reports_path + '/Strategy' + strat)]
    for file in strat_files_list:
        with open(csv_reports_path + '/Strategy' + strat + '/' + file) as json_file:
            data = json.load(json_file)
            data = [seq for seq in data if seq["exit code"] != 0]
            with open("Strategy" + strat + "/" + strat + file, 'w') as outfile:
                json.dump(data, outfile, indent=4)