Strategy1, Strategy2, Strategy3 are the files that contain the json files for each number of
sequences vs number of commands. The matrix of iterations is the following: [10, 100, 500, 1000]
sequences x [5, 10, 50, 100] commands. So there must be 16 files for each folder.

The JSON object represented on each file is a list of sequences of commands. Each sequence is a
dictionary that contains a list of dictionaries with the sequences of commands sent, the exit code
of the process, the execution time, and memory used.

filter_reports2.py helped to generate the file.

