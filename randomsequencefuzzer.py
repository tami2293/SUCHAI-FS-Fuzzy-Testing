from fuzzingbook.Fuzzer import RandomFuzzer
from flightsoftwarerunner import *
import random


class RandomSequenceFuzzer(RandomFuzzer):
    def __init__(self, min_length=10, max_length=100,
                 char_start=32, char_range=32, n_cmds=1):
        RandomFuzzer.__init__(self, min_length, max_length, char_start, char_range)
        self.n_cmds = n_cmds

    def run(self, runner=FlightSoftwareRunner()):
        """Run `runner` with fuzz input"""
        cmds_list = ["com_ping", "com_set_node", "test", "drp_ebf", "drp_add_hrs_alive", "drp_set_deployed",
                     "tm_get_last", "tm_send_status"]
        cmds_to_send = []
        params_to_send = []
        for i in range(0, self.n_cmds):
            cmds_to_send.append(random.choice(cmds_list))
            params_to_send.append(self.fuzz())
        return runner.run(cmds_to_send, params_to_send)
