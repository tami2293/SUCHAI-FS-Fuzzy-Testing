from fuzzingbook.Fuzzer import RandomFuzzer
from flightsoftwarerunner import *
import random


class RandomSequenceFuzzer(RandomFuzzer):
    def __init__(self, min_length=10, max_length=100,
                 char_start=32, char_range=32, n_cmds=1, fs_cmds=["help"]):
        RandomFuzzer.__init__(self, min_length, max_length, char_start, char_range)
        self.n_cmds = n_cmds
        self.fs_cmds = fs_cmds

    def run(self, runner=FlightSoftwareRunner()):
        """
        Run 'runner' with fuzzed parameters and random commands chosen from a list
        :param runner:
        :return: Results obtained from running the program with fuzzed input
        """
        cmds_to_send = []
        params_to_send = []
        print(self.fs_cmds)
        for i in range(0, self.n_cmds):
            cmds_to_send.append(random.choice(self.fs_cmds))
            n_params = random.randint(0, 11)  # 11 is the max number of params that a cmd has
            params = [self.fuzz() for i in range(n_params)]
            params = " ".join(params)
            params_to_send.append(params)
        return runner.run_process(cmds_to_send, params_to_send)
