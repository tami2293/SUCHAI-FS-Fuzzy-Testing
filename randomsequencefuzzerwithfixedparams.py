from randomsequencefuzzer import *


class RandomSequenceFuzzerWithFixedParams(RandomSequenceFuzzer):
    def __init__(self, number_of_params, min_length=10, max_length=100,
                 char_start=32, char_range=32, n_cmds=1, fs_cmds=["help"]):
        RandomSequenceFuzzer.__init__(self, min_length, max_length, char_start, char_range, n_cmds, fs_cmds)
        self.number_of_params = number_of_params

    def run(self, runner=FlightSoftwareRunner()):
        """
        Run 'runner' with fuzzed parameters and random commands chosen from a list
        :param runner:
        :return: Results obtained from running the program with fuzzed input
        """
        self.fuzz_funcs = [self.fuzz_int, self.fuzz_float, self.fuzz_long, self.fuzz_unsigned_int, self.fuzz_string]
        cmds_to_send = []
        params_to_send = []
        print(self.fs_cmds)
        for i in range(0, self.n_cmds):
            ind_chosen = random.randint(0, len(self.fs_cmds) - 1)
            cmds_to_send.append(self.fs_cmds[ind_chosen])
            n_params = self.number_of_params[ind_chosen]
            fuzz_to_apply = [random.choice(self.fuzz_funcs) for i in range(n_params)]
            params = [fuzz_to_apply[i]() for i in range(n_params)]
            params = " ".join(params)
            params_to_send.append(params)
        return runner.run_process(cmds_to_send, params_to_send)