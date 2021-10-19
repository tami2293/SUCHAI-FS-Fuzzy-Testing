from randomsequencefuzzer import *


class RandomSequenceFuzzerWithFixedParamsAndExactTypes(RandomSequenceFuzzer):
    def __init__(self, commands_filename, min_length=10, max_length=100,
                 char_start=32, char_range=32, n_cmds=1):
        RandomSequenceFuzzer.__init__(self, commands_filename, min_length, max_length, char_start, char_range, n_cmds)
        self.params_types = []
        self.get_parameters_types(self.commands_file)

    def get_parameters_types(self, commands_list):
        parameters_types = []
        with open(commands_list) as file_list:
            for row in file_list:
                params_str_without_newline = row.rstrip('\n')
                parameters_types.append(params_str_without_newline.split(', ')[2:])
        self.params_types = parameters_types

    def run(self, runner=FlightSoftwareRunner()):
        """
        Run 'runner' with fuzzed parameters and random commands chosen from a list
        :param runner:
        :return: Results obtained from running the program with fuzzed input
        """
        self.types_dic = {"% d": self.fuzz_int, "% i": self.fuzz_int, "% f": self.fuzz_float, "% ld": self.fuzz_long,
                          "% u": self.fuzz_unsigned_int, "% s": self.fuzz_string, "% n": self.fuzz_string,
                          "% p": self.fuzz_string, }
        cmds_to_send = []
        params_to_send = []
        print(self.fs_cmds)
        for i in range(0, self.n_cmds):
            ind_chosen = random.randint(0, len(self.fs_cmds) - 1)
            cmds_to_send.append(self.fs_cmds[ind_chosen])  # Append the command
            n_params = len(self.params_types[ind_chosen])  # Determine parameters number of the command
            fuzz_to_apply = [self.types_dic[self.params_types[ind_chosen][j]] for j in range(n_params)]  # Choose fuzz function for each parameter type of the command
            params = [fuzz_to_apply[i]() for i in range(n_params)]  # Run each fuzz function
            params = " ".join(params)
            params_to_send.append(params)
        return runner.run_process(cmds_to_send, params_to_send)
