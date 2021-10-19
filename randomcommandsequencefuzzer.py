from fuzzingbook.Fuzzer import RandomFuzzer
from flightsoftwarerunner import *


class RandomCommandsSequenceFuzzer(RandomFuzzer):
    def __init__(self, commands_filename, min_length=10, max_length=100, char_start=0, char_range=127, n_cmds=1):
        RandomFuzzer.__init__(self, min_length, max_length, char_start, char_range)
        self.n_cmds = n_cmds
        self.commands_file = commands_filename

    def run(self, runner=FlightSoftwareRunner()):
        """
        Run 'runner' with fuzzed parameters and random commands chosen from a list
        :param runner:
        :return: Results obtained from running the program with fuzzed input
        """
        cmds_to_send = []
        params_to_send = []
        for i in range(0, self.n_cmds):
            cmds_to_send.append(self.fuzz())
            params = ""
            params_to_send.append(params)
        return runner.run_process(cmds_to_send, params_to_send)
